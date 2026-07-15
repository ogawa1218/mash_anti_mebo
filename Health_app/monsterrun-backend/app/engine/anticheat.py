"""ヒューリスティック・アンチチートエンジン。

スコアベース設計: 各ヒューリスティックが重み付きフラグを返し、合計 cheat_score で判定。
  score ≥ 50 → quarantined（EXP付与なし・保持して再判定可能）
  25–49     → flagged（付与するが監査対象）
  <25       → accepted

検知対象:
  H1 乗り物移動: 人間として不可能な持続速度（>25km/h が 120s 以上）
  H2 乗り物移動: 速度≥15km/h なのに心拍が安静時+15bpm未満（自転車・車・電車）
  H3 シェイカー: 歩数から逆算したストライド長が生理的範囲外
  H4 シェイカー: 歩数があるのにGPS変位ほぼゼロ & 心拍平坦
  H5 GPS偽装 : テレポート（隣接点間の瞬間速度スパイク / 非物理的加速度）
"""

import math
from dataclasses import dataclass, field

from app.schemas.activity import GPSSample, NormalizedActivity

# --- 閾値定数 ---------------------------------------------------------------
VEHICLE_SPEED_KMH = 25.0        # H1: これ以上の持続速度は乗り物（エリート短距離でも維持不可）
VEHICLE_SUSTAIN_S = 120         # H1: 持続判定時間
HR_SPEED_MIN_KMH = 15.0         # H2: この速度で
HR_SPEED_RESTING_MARGIN = 15    # H2: HR < hr_rest+15 なら受動移動
STRIDE_MIN_M = 0.35             # H3: 歩幅下限（シャッフル歩行）
STRIDE_MAX_M = 2.60             # H3: 歩幅上限（エリートスプリント）
SHAKER_MIN_STEPS = 500          # H4: 判定対象の最低歩数
SHAKER_MAX_DISPLACEMENT_M = 80.0  # H4: この変位以下でGPS静止とみなす
SHAKER_HR_STD_MAX = 5.0         # H4: 心拍標準偏差がこれ未満なら「平坦」
TELEPORT_SPEED_KMH = 60.0       # H5: 瞬間速度スパイク
MAX_HUMAN_ACCEL_MS2 = 3.0       # H5: 持続加速度の上限
GPS_MIN_POINTS = 5              # GPS系判定に必要な最低点数

QUARANTINE_THRESHOLD = 50
FLAG_THRESHOLD = 25


@dataclass(frozen=True)
class CheatFlag:
    code: str
    weight: int
    detail: str


@dataclass(frozen=True)
class CheatVerdict:
    score: int                      # 0–100
    status: str                     # accepted | flagged | quarantined
    flags: list[CheatFlag] = field(default_factory=list)

    def as_json(self) -> list[dict]:
        return [{"code": f.code, "weight": f.weight, "detail": f.detail} for f in self.flags]


def haversine_m(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    r = 6_371_000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _segment_speeds(gps: list[GPSSample]) -> list[tuple[float, float]]:
    """隣接GPS点間の (速度km/h, 区間秒数)。時刻順ソート済み前提。低精度点はスキップ。"""
    out = []
    for a, b in zip(gps, gps[1:]):
        dt = b.t - a.t
        if dt <= 0:
            continue
        if (a.h_acc_m or 0) > 50 or (b.h_acc_m or 0) > 50:
            continue  # 水平精度50m超は信頼しない
        dist = haversine_m(a.lat, a.lng, b.lat, b.lng)
        out.append((dist / dt * 3.6, float(dt)))
    return out


class AntiCheatEngine:
    """NormalizedActivity 1件を評価して CheatVerdict を返す。副作用なし・純関数。"""

    def evaluate(self, act: NormalizedActivity, hr_rest: int) -> CheatVerdict:
        flags: list[CheatFlag] = []
        gps = sorted(act.gps_samples, key=lambda s: s.t)
        speeds = _segment_speeds(gps) if len(gps) >= GPS_MIN_POINTS else []

        for check in (
            lambda: self._h1_impossible_speed(act, speeds),
            lambda: self._h2_hr_speed_mismatch(act, hr_rest),
            lambda: self._h3_stride_length(act),
            lambda: self._h4_shaker(act, gps),
            lambda: self._h5_gps_teleport(speeds),
        ):
            if (flag := check()) is not None:
                flags.append(flag)

        score = min(sum(f.weight for f in flags), 100)
        if score >= QUARANTINE_THRESHOLD:
            status = "quarantined"
        elif score >= FLAG_THRESHOLD:
            status = "flagged"
        else:
            status = "accepted"
        return CheatVerdict(score=score, status=status, flags=flags)

    # --- H1: 人間として不可能な持続速度 -------------------------------------
    def _h1_impossible_speed(
        self, act: NormalizedActivity, speeds: list[tuple[float, float]]
    ) -> CheatFlag | None:
        if act.activity_type in ("ride",):  # 自転車は対象外
            return None
        # GPS区間ベース: >25km/h の連続滞在秒数を計測
        sustained = 0.0
        for kmh, dt in speeds:
            if kmh > VEHICLE_SPEED_KMH:
                sustained += dt
                if sustained >= VEHICLE_SUSTAIN_S:
                    return CheatFlag(
                        "H1_IMPOSSIBLE_SPEED", 40,
                        f">{VEHICLE_SPEED_KMH}km/h が {int(sustained)}s 継続（乗り物移動の疑い）",
                    )
            else:
                sustained = 0.0
        # GPSがない場合のフォールバック: 平均速度
        if not speeds and act.duration_s > VEHICLE_SUSTAIN_S:
            avg_kmh = act.distance_m / act.duration_s * 3.6
            if avg_kmh > VEHICLE_SPEED_KMH:
                return CheatFlag(
                    "H1_IMPOSSIBLE_SPEED", 40,
                    f"平均 {avg_kmh:.1f}km/h（GPSなし・距離/時間から算出）",
                )
        return None

    # --- H2: 心拍と速度の相関矛盾 --------------------------------------------
    def _h2_hr_speed_mismatch(self, act: NormalizedActivity, hr_rest: int) -> CheatFlag | None:
        if act.hr_avg is None or act.duration_s <= 0 or act.activity_type == "ride":
            return None
        avg_kmh = act.distance_m / act.duration_s * 3.6
        if avg_kmh >= HR_SPEED_MIN_KMH and act.hr_avg < hr_rest + HR_SPEED_RESTING_MARGIN:
            return CheatFlag(
                "H2_HR_SPEED_MISMATCH", 35,
                f"{avg_kmh:.1f}km/h 移動中の平均心拍 {act.hr_avg}bpm は安静時"
                f"({hr_rest}bpm)+{HR_SPEED_RESTING_MARGIN} 未満（自動車・自転車移動とみなす）",
            )
        return None

    # --- H3: ストライド長の生理的整合性 --------------------------------------
    def _h3_stride_length(self, act: NormalizedActivity) -> CheatFlag | None:
        if not act.steps or act.steps < 100 or act.distance_m < 100:
            return None
        stride = act.distance_m / act.steps
        if stride < STRIDE_MIN_M or stride > STRIDE_MAX_M:
            return CheatFlag(
                "H3_STRIDE_ANOMALY", 30,
                f"歩幅 {stride:.2f}m が範囲外({STRIDE_MIN_M}–{STRIDE_MAX_M}m)。"
                "シェイカーまたはGPS距離偽装の疑い",
            )
        return None

    # --- H4: シェイカー（歩数あり・GPS静止・心拍平坦） ------------------------
    def _h4_shaker(self, act: NormalizedActivity, gps: list[GPSSample]) -> CheatFlag | None:
        if not act.steps or act.steps < SHAKER_MIN_STEPS or len(gps) < GPS_MIN_POINTS:
            return None
        # 開始点からの最大変位
        origin = gps[0]
        max_disp = max(haversine_m(origin.lat, origin.lng, p.lat, p.lng) for p in gps)
        if max_disp > SHAKER_MAX_DISPLACEMENT_M:
            return None
        # 心拍の平坦性（運動していれば揺らぐ）
        bpms = [s.bpm for s in act.hr_samples]
        hr_flat = len(bpms) >= 10 and _std(bpms) < SHAKER_HR_STD_MAX
        if hr_flat or not bpms:
            return CheatFlag(
                "H4_SHAKER_PATTERN", 30,
                f"歩数{act.steps}に対しGPS変位{max_disp:.0f}m・心拍平坦。物理シェイカーの疑い",
            )
        return None

    # --- H5: GPSテレポート/非物理的加速度 ------------------------------------
    def _h5_gps_teleport(self, speeds: list[tuple[float, float]]) -> CheatFlag | None:
        if len(speeds) < 2:
            return None
        spikes = sum(1 for kmh, _ in speeds if kmh > TELEPORT_SPEED_KMH)
        if spikes >= 2:
            return CheatFlag(
                "H5_GPS_TELEPORT", 25,
                f"瞬間速度 >{TELEPORT_SPEED_KMH}km/h のスパイクが {spikes} 回（座標ジャンプ）",
            )
        for (v1, _), (v2, dt2) in zip(speeds, speeds[1:]):
            accel = abs(v2 - v1) / 3.6 / max(dt2, 1)
            if accel > MAX_HUMAN_ACCEL_MS2:
                return CheatFlag(
                    "H5_GPS_TELEPORT", 25,
                    f"加速度 {accel:.1f}m/s² は人間の走行範囲外（GPS偽装の疑い）",
                )
        return None


def _std(values: list[int]) -> float:
    n = len(values)
    mean = sum(values) / n
    return math.sqrt(sum((v - mean) ** 2 for v in values) / n)
