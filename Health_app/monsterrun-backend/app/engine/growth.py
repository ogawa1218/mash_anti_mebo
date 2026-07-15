"""成長数理エンジン。

    EXP = d × (HR_avg / HR_rest) × C_temp × α × novice_bonus × effect_multiplier

設計意図 — 「運動初心者が優遇される」:
1. HR_avg/HR_rest 比は、同じ絶対ペースでも心肺が未発達な初心者ほど大きくなる。
   つまり式そのものが相対努力ベースで、上級者のイージーランより
   初心者の全力ジョグのほうが多くEXPを得る。
2. novice_bonus は生涯累積距離への指数減衰。開始直後 ×1.5 → 1,000km で ≈×1.0。
   継続体験の立ち上がり（最初の30日）を厚くする。
3. 心拍比はクリップ(上限3.5)し、異常値・チートでの爆発を防ぐ。
"""

from dataclasses import dataclass, field
from math import exp as _exp

# --- チューニング定数 -------------------------------------------------------
HR_RATIO_CAP = 3.5          # HR_avg/HR_rest の上限（安全クリップ）
HR_RATIO_FLOOR = 1.0        # 安静時未満は1.0扱い
NOVICE_MAX_BONUS = 0.5      # 開始時の追加倍率 (=×1.5)
NOVICE_DECAY_KM = 350.0     # e^-1 になる累積距離
LEVEL_BASE_EXP = 100.0      # Lv2に必要なEXP
LEVEL_GROWTH = 1.15         # レベル毎の必要EXP逓増率


@dataclass(frozen=True)
class ExpInput:
    distance_km: float
    hr_avg: int | None          # 心拍欠損時は控えめな固定係数で計算
    hr_rest: int
    temperature_c: float | None
    lifetime_distance_km: float # novice_bonus 用
    alpha: float = 10.0
    effect_multiplier: float = 1.0  # 栄養Buff/Debuff（monster_effects の積）


@dataclass(frozen=True)
class ExpResult:
    exp: float
    hr_ratio: float
    c_temp: float
    novice_bonus: float
    breakdown: dict = field(default_factory=dict)


def temperature_correction(temperature_c: float | None) -> float:
    """環境補正 C_temp。快適域(10–18°C)=1.0、暑熱・寒冷ほど生理的負荷が増すため加点。

    WBGTの簡易近似: 快適域から1°C離れるごとに +1.25%、上限 +15%。
    """
    if temperature_c is None:
        return 1.0
    if 10.0 <= temperature_c <= 18.0:
        return 1.0
    dist = (10.0 - temperature_c) if temperature_c < 10.0 else (temperature_c - 18.0)
    return round(min(1.0 + dist * 0.0125, 1.15), 4)


def novice_bonus(lifetime_distance_km: float) -> float:
    """生涯累積距離に対する指数減衰ボーナス。0km → 1.5、350km → ≈1.18、1000km → ≈1.03。"""
    return round(1.0 + NOVICE_MAX_BONUS * _exp(-max(lifetime_distance_km, 0.0) / NOVICE_DECAY_KM), 4)


def hr_ratio(hr_avg: int | None, hr_rest: int) -> float:
    """相対心拍努力。欠損時は 1.4（緩いジョグ相当）の保守値。"""
    if hr_avg is None:
        return 1.4
    return round(min(max(hr_avg / max(hr_rest, 30), HR_RATIO_FLOOR), HR_RATIO_CAP), 4)


def calc_exp(inp: ExpInput) -> ExpResult:
    """EXP = d × (HR_avg/HR_rest) × C_temp × α × novice_bonus × effect_multiplier"""
    ratio = hr_ratio(inp.hr_avg, inp.hr_rest)
    c_temp = temperature_correction(inp.temperature_c)
    novice = novice_bonus(inp.lifetime_distance_km)
    effect = min(max(inp.effect_multiplier, 0.1), 2.0)  # Buff積の暴走防止

    exp_value = inp.distance_km * ratio * c_temp * inp.alpha * novice * effect
    return ExpResult(
        exp=round(exp_value, 2),
        hr_ratio=ratio,
        c_temp=c_temp,
        novice_bonus=novice,
        breakdown={
            "d_km": inp.distance_km,
            "hr_ratio": ratio,
            "c_temp": c_temp,
            "alpha": inp.alpha,
            "novice_bonus": novice,
            "effect_multiplier": effect,
        },
    )


# --- レベルカーブ -----------------------------------------------------------

def exp_required_for_level(level: int) -> float:
    """Lv(n) → Lv(n+1) に必要なEXP。100 × 1.15^(n-1)。"""
    return round(LEVEL_BASE_EXP * (LEVEL_GROWTH ** (level - 1)), 2)


def apply_exp_to_level(current_level: int, current_exp: float, gained: float) -> tuple[int, float]:
    """余剰EXPを繰り越しながらレベルアップ。(new_level, leftover_exp) を返す。"""
    level, pool = current_level, current_exp + gained
    while level < 100 and pool >= exp_required_for_level(level):
        pool -= exp_required_for_level(level)
        level += 1
    return level, round(pool, 2)
