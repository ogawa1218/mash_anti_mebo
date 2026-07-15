-- =============================================================================
-- Project MonsterRun — Initial Schema (PostgreSQL 16)
-- 適用: psql "$DATABASE_URL" -f migrations/001_initial_schema.sql
-- =============================================================================

BEGIN;

CREATE EXTENSION IF NOT EXISTS "pgcrypto";      -- gen_random_uuid()

-- ---------------------------------------------------------------------------
-- ENUM 型
-- ---------------------------------------------------------------------------
CREATE TYPE wearable_source AS ENUM ('garmin', 'strava', 'apple_healthkit', 'google_health_connect', 'manual');
CREATE TYPE activity_status AS ENUM ('pending', 'accepted', 'flagged', 'quarantined', 'rejected', 'duplicate');
CREATE TYPE activity_type   AS ENUM ('run', 'walk', 'ride', 'swim', 'strength', 'hike', 'other');
CREATE TYPE evolution_line  AS ENUM ('balanced', 'stamina_guardian', 'speed_striker');
CREATE TYPE monster_anim    AS ENUM ('idle', 'happy', 'tired', 'training', 'evolving', 'sick', 'sleeping');
CREATE TYPE effect_kind     AS ENUM ('buff', 'debuff');

-- ---------------------------------------------------------------------------
-- Users / Auth
-- ---------------------------------------------------------------------------
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           TEXT NOT NULL UNIQUE,
    display_name    TEXT NOT NULL,
    password_hash   TEXT,                          -- NULL = ソーシャルログインのみ
    date_of_birth   DATE,                          -- 最大心拍推定 (220-age) に使用
    sex             TEXT CHECK (sex IN ('male', 'female', 'other')),
    height_cm       NUMERIC(5,1),
    weight_kg       NUMERIC(5,1),                  -- BMR計算・g/kgタンパク質判定に使用
    hr_rest         SMALLINT NOT NULL DEFAULT 60 CHECK (hr_rest BETWEEN 30 AND 120),
    hr_max          SMALLINT CHECK (hr_max BETWEEN 120 AND 230),
    timezone        TEXT NOT NULL DEFAULT 'Asia/Tokyo',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ウェアラブル連携（OAuth 2.0 トークン。トークン本体はアプリ層でFernet暗号化した文字列を格納）
CREATE TABLE wearable_connections (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    source                  wearable_source NOT NULL,
    provider_user_id        TEXT NOT NULL,          -- Garmin userAccessToken / Strava athlete_id 等
    access_token_enc        TEXT NOT NULL,          -- Fernet暗号化済み
    refresh_token_enc       TEXT,
    token_expires_at        TIMESTAMPTZ,
    scopes                  TEXT[] NOT NULL DEFAULT '{}',
    is_active               BOOLEAN NOT NULL DEFAULT TRUE,
    last_synced_at          TIMESTAMPTZ,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source, provider_user_id),              -- Webhook→内部ユーザー逆引き
    UNIQUE (user_id, source)
);
CREATE INDEX idx_wc_provider_lookup ON wearable_connections (source, provider_user_id) WHERE is_active;

-- 生Webhookペイロード（監査・再処理用）
CREATE TABLE raw_payloads (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source          wearable_source NOT NULL,
    external_id     TEXT,
    payload         JSONB NOT NULL,
    received_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    processed_at    TIMESTAMPTZ
);
CREATE INDEX idx_raw_unprocessed ON raw_payloads (received_at) WHERE processed_at IS NULL;

-- ---------------------------------------------------------------------------
-- WearableActivities: 正規化済みアクティビティ
-- ---------------------------------------------------------------------------
CREATE TABLE wearable_activities (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    source              wearable_source NOT NULL,
    external_id         TEXT NOT NULL,              -- ソース側の活動ID
    activity_type       activity_type NOT NULL DEFAULT 'run',
    started_at          TIMESTAMPTZ NOT NULL,
    ended_at            TIMESTAMPTZ NOT NULL,
    duration_s          INTEGER NOT NULL CHECK (duration_s > 0),
    distance_m          NUMERIC(10,1) NOT NULL DEFAULT 0,
    steps               INTEGER,
    calories_active     NUMERIC(7,1),               -- アクティブエネルギー kcal
    hr_avg              SMALLINT,
    hr_max              SMALLINT,
    hr_samples          JSONB,                      -- [{"t": epoch_s, "bpm": int}, ...] ダウンサンプル済み
    gps_polyline        TEXT,                       -- encoded polyline（生軌跡は原則保持しない）
    gps_samples         JSONB,                      -- [{"t","lat","lng","alt"}] アンチチート用ダウンサンプル
    elevation_gain_m    NUMERIC(6,1),
    temperature_c       NUMERIC(4,1),               -- 環境補正 C_temp 用
    status              activity_status NOT NULL DEFAULT 'pending',
    cheat_score         SMALLINT NOT NULL DEFAULT 0 CHECK (cheat_score BETWEEN 0 AND 100),
    cheat_flags         JSONB NOT NULL DEFAULT '[]',-- [{"code":"H2_HR_SPEED_MISMATCH","weight":35,...}]
    exp_awarded         NUMERIC(10,2),              -- NULL = 未計算
    zone_seconds        JSONB,                      -- {"z1":..,"z2":..,"z3":..,"z4":..,"z5":..}
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source, external_id)                    -- 冪等インジェスト
);
CREATE INDEX idx_activities_user_time ON wearable_activities (user_id, started_at DESC);
CREATE INDEX idx_activities_status    ON wearable_activities (status) WHERE status IN ('pending', 'flagged');

-- EXP台帳（二重付与防止・再計算可能な唯一の真実）
CREATE TABLE exp_ledger (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    monster_id      UUID NOT NULL,                  -- FK は monsters 定義後に追加
    activity_id     UUID REFERENCES wearable_activities(id) ON DELETE SET NULL,
    idempotency_key TEXT NOT NULL UNIQUE,           -- "activity:{id}" or "mcp:{key}"
    exp_delta       NUMERIC(10,2) NOT NULL,
    stamina_delta   NUMERIC(8,2) NOT NULL DEFAULT 0,
    speed_delta     NUMERIC(8,2) NOT NULL DEFAULT 0,
    reason          TEXT NOT NULL,                  -- "activity" | "mcp_coaching" | "nutrition_bonus"
    metadata        JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- Monsters
-- ---------------------------------------------------------------------------
CREATE TABLE monsters (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name                TEXT NOT NULL,
    species_code        TEXT NOT NULL DEFAULT 'runmon_baby',   -- 見た目/種族マスタへの参照
    generation          SMALLINT NOT NULL DEFAULT 1,
    level               SMALLINT NOT NULL DEFAULT 1 CHECK (level BETWEEN 1 AND 100),
    exp                 NUMERIC(12,2) NOT NULL DEFAULT 0,
    -- コアステータス
    stamina             NUMERIC(8,2) NOT NULL DEFAULT 10,
    agility             NUMERIC(8,2) NOT NULL DEFAULT 10,
    attack              NUMERIC(8,2) NOT NULL DEFAULT 10,
    defense             NUMERIC(8,2) NOT NULL DEFAULT 10,
    heart_points        NUMERIC(8,2) NOT NULL DEFAULT 100,     -- HP相当。コンディションで増減
    -- 進化
    evolution_line      evolution_line NOT NULL DEFAULT 'balanced',
    evolution_gauge     NUMERIC(6,2) NOT NULL DEFAULT 0 CHECK (evolution_gauge BETWEEN 0 AND 100),
    stamina_points      NUMERIC(10,2) NOT NULL DEFAULT 0,      -- LSD蓄積
    speed_points        NUMERIC(10,2) NOT NULL DEFAULT 0,      -- HIIT蓄積
    -- 状態
    condition_score     SMALLINT NOT NULL DEFAULT 70 CHECK (condition_score BETWEEN 0 AND 100),
    animation_state     monster_anim NOT NULL DEFAULT 'idle',
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,         -- 1ユーザー同時1体
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX idx_one_active_monster ON monsters (user_id) WHERE is_active;

ALTER TABLE exp_ledger
    ADD CONSTRAINT fk_ledger_monster FOREIGN KEY (monster_id) REFERENCES monsters(id) ON DELETE CASCADE;
CREATE INDEX idx_ledger_monster ON exp_ledger (monster_id, created_at DESC);

-- バフ・デバフ（栄養エンジン/MCPコーチングが付与）
CREATE TABLE monster_effects (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    monster_id      UUID NOT NULL REFERENCES monsters(id) ON DELETE CASCADE,
    kind            effect_kind NOT NULL,
    code            TEXT NOT NULL,                  -- 'protein_boost' | 'underfueled' | 'sugar_crash' ...
    exp_multiplier  NUMERIC(4,2) NOT NULL DEFAULT 1.00,
    stat_modifiers  JSONB NOT NULL DEFAULT '{}',    -- {"stamina": +0.05, ...}
    granted_by      TEXT NOT NULL,                  -- 'nutrition_engine' | 'mcp:grant_coaching_buff'
    expires_at      TIMESTAMPTZ NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_effects_active ON monster_effects (monster_id, expires_at);

-- 進化履歴
CREATE TABLE evolution_history (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    monster_id      UUID NOT NULL REFERENCES monsters(id) ON DELETE CASCADE,
    from_species    TEXT NOT NULL,
    to_species      TEXT NOT NULL,
    line            evolution_line NOT NULL,
    stamina_points  NUMERIC(10,2) NOT NULL,
    speed_points    NUMERIC(10,2) NOT NULL,
    evolved_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- NutritionLogs
-- ---------------------------------------------------------------------------
CREATE TABLE nutrition_logs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    log_date        DATE NOT NULL,
    source          TEXT NOT NULL DEFAULT 'manual', -- 'myfitnesspal' | 'cronometer' | 'manual'
    calories_in     NUMERIC(7,1) NOT NULL CHECK (calories_in >= 0),
    protein_g       NUMERIC(6,1) NOT NULL DEFAULT 0,
    fat_g           NUMERIC(6,1) NOT NULL DEFAULT 0,
    carbs_g         NUMERIC(6,1) NOT NULL DEFAULT 0,
    meals           JSONB NOT NULL DEFAULT '[]',    -- [{"name","time","kcal","p","f","c"}]
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (user_id, log_date, source)
);
CREATE INDEX idx_nutrition_user_date ON nutrition_logs (user_id, log_date DESC);

-- 日次サマリ（栄養エンジンの出力キャッシュ。コンディション履歴）
CREATE TABLE daily_condition_snapshots (
    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    snapshot_date       DATE NOT NULL,
    energy_balance_kcal NUMERIC(7,1) NOT NULL,
    pfc_score           SMALLINT NOT NULL,          -- 0-100
    condition_score     SMALLINT NOT NULL,
    effects_applied     JSONB NOT NULL DEFAULT '[]',
    PRIMARY KEY (user_id, snapshot_date)
);

-- updated_at 自動更新トリガ
CREATE OR REPLACE FUNCTION touch_updated_at() RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = now(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_touch    BEFORE UPDATE ON users               FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
CREATE TRIGGER trg_wc_touch       BEFORE UPDATE ON wearable_connections FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
CREATE TRIGGER trg_monsters_touch BEFORE UPDATE ON monsters            FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
CREATE TRIGGER trg_nutrition_touch BEFORE UPDATE ON nutrition_logs     FOR EACH ROW EXECUTE FUNCTION touch_updated_at();

COMMIT;
