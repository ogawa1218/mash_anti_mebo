"""進化分岐エンジン — 心拍ゾーン滞在時間を進化ポイントへ変換する。

Karvonen法（心拍予備能 HRR%）:
    HRR% = (HR - HR_rest) / (HR_max - HR_rest)

| ゾーン | HRR%    | 性質            | 蓄積先           |
|--------|---------|-----------------|------------------|
| Z1     | <60%    | 回復走          | stamina ×0.5     |
| Z2     | 60–70%  | LSD             | stamina ×1.0     |
| Z3     | 70–80%  | テンポ走        | 両方 ×0.5        |
| Z4     | 80–90%  | 閾値/インターバル| speed ×1.0       |
| Z5     | ≥90%    | VO2max/レペ     | speed ×1.5       |

進化ゲージが100に達した時点の speed/stamina 比で分岐先を決定する。
"""

from dataclasses import dataclass

from app.schemas.activity import HRSample

GAUGE_FULL = 100.0
GAUGE_PER_POINT = 0.10          # 進化P 1あたりゲージ+0.1（= 合計1000Pで進化）
BRANCH_DOMINANCE = 1.35         # 一方が他方の1.35倍以上で特化型に分岐

ZONE_BOUNDS = [0.60, 0.70, 0.80, 0.90]  # HRR% の Z1/Z2/Z3/Z4/Z5 境界
POINTS_PER_MIN = 1.0            # ゾーン滞在1分あたりの基礎ポイント

ZONE_WEIGHTS = {  # zone -> (stamina係数, speed係数)
    "z1": (0.5, 0.0),
    "z2": (1.0, 0.0),
    "z3": (0.5, 0.5),
    "z4": (0.0, 1.0),
    "z5": (0.0, 1.5),
}


@dataclass(frozen=True)
class EvolutionDelta:
    stamina_points: float
    speed_points: float
    zone_seconds: dict[str, int]


def classify_zone(bpm: int, hr_rest: int, hr_max: int) -> str:
    hrr = (bpm - hr_rest) / max(hr_max - hr_rest, 1)
    for i, bound in enumerate(ZONE_BOUNDS):
        if hrr < bound:
            return f"z{i + 1}"
    return "z5"


def zone_seconds_from_samples(samples: list[HRSample], hr_rest: int, hr_max: int) -> dict[str, int]:
    """時系列心拍サンプル → 各ゾーン滞在秒数。サンプル間隔は隣接差分（上限60s）で推定。"""
    zones = {f"z{i}": 0 for i in range(1, 6)}
    for i, s in enumerate(samples):
        if i + 1 < len(samples):
            dt = min(max(samples[i + 1].t - s.t, 1), 60)
        else:
            dt = 5  # 末尾はダウンサンプル間隔の既定値
        zones[classify_zone(s.bpm, hr_rest, hr_max)] += dt
    return zones


def zone_seconds_from_avg(hr_avg: int, duration_s: int, hr_rest: int, hr_max: int) -> dict[str, int]:
    """サンプル欠損時のフォールバック: 平均心拍のゾーンに全時間を割り当てる。"""
    zones = {f"z{i}": 0 for i in range(1, 6)}
    zones[classify_zone(hr_avg, hr_rest, hr_max)] = duration_s
    return zones


def evolution_points(zone_seconds: dict[str, int]) -> EvolutionDelta:
    """ゾーン滞在時間 → LSD=スタミナ / HIIT=スピード の進化ポイント。"""
    stamina = speed = 0.0
    for zone, seconds in zone_seconds.items():
        w_sta, w_spd = ZONE_WEIGHTS.get(zone, (0.0, 0.0))
        minutes = seconds / 60.0
        stamina += minutes * POINTS_PER_MIN * w_sta
        speed += minutes * POINTS_PER_MIN * w_spd
    return EvolutionDelta(round(stamina, 2), round(speed, 2), zone_seconds)


def gauge_increment(delta: EvolutionDelta) -> float:
    return round((delta.stamina_points + delta.speed_points) * GAUGE_PER_POINT, 2)


def decide_branch(stamina_points: float, speed_points: float) -> str:
    """ゲージ満了時の分岐判定。拮抗時は balanced。"""
    if stamina_points >= speed_points * BRANCH_DOMINANCE:
        return "stamina_guardian"
    if speed_points >= stamina_points * BRANCH_DOMINANCE:
        return "speed_striker"
    return "balanced"


# 分岐 → 次世代種族コードとステータス倍率（種族マスタの簡易版）
EVOLUTION_TABLE: dict[str, dict] = {
    "stamina_guardian": {
        "species_suffix": "guardian",
        "stat_bonus": {"stamina": 1.30, "defense": 1.25, "agility": 1.00, "attack": 1.05},
    },
    "speed_striker": {
        "species_suffix": "striker",
        "stat_bonus": {"stamina": 1.05, "defense": 1.00, "agility": 1.30, "attack": 1.25},
    },
    "balanced": {
        "species_suffix": "harmony",
        "stat_bonus": {"stamina": 1.15, "defense": 1.15, "agility": 1.15, "attack": 1.15},
    },
}
