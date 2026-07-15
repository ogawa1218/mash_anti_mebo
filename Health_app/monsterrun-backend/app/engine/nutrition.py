"""栄養エンジン — カロリー収支とPFCバランスをモンスターのコンディション/Buff/Debuffへ変換。

設計方針:
- 「食べなければ痩せてEXPが増える」構造にしない。過度な欠損は underfueled デバフ
  （EXP−30%）になり、健康的な収支・十分なタンパク質こそが最強のバフになる。
- ターゲット層（減量中の30–40代）を想定し、適正な緩やかな欠損(−300±200kcal)を最高評価とする。
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from app.schemas.nutrition import ConditionResult

# PFC 目標比率（減量期の標準値）
PFC_TARGET = {"protein": 0.30, "fat": 0.25, "carbs": 0.45}
KCAL_PER_G = {"protein": 4.0, "fat": 9.0, "carbs": 4.0}

IDEAL_DEFICIT_KCAL = -300.0      # 減量に最適な収支
DEFICIT_TOLERANCE = 200.0        # ±この範囲は満点
SEVERE_DEFICIT_KCAL = -800.0     # これ以下は underfueled
SURPLUS_LIMIT_KCAL = 400.0       # これ以上の過剰は overfed
PROTEIN_BOOST_G_PER_KG = 1.6     # タンパク質バフ閾値
SUGAR_CRASH_CARB_RATIO = 0.65    # 炭水化物比率がこれ超で sugar_crash


@dataclass(frozen=True)
class NutritionInput:
    calories_in: float
    protein_g: float
    fat_g: float
    carbs_g: float
    active_calories: float   # 当日のアクティブ消費 (wearable_activities 合計)
    bmr_kcal: float          # 基礎代謝（Mifflin-St Jeor）
    weight_kg: float


def bmr_mifflin_st_jeor(weight_kg: float, height_cm: float, age: int, sex: str) -> float:
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    return base + (5 if sex == "male" else -161)


def pfc_score(inp: NutritionInput) -> int:
    """PFC実績比率と目標比率の乖離をスコア化（0–100）。"""
    total_kcal = (
        inp.protein_g * KCAL_PER_G["protein"]
        + inp.fat_g * KCAL_PER_G["fat"]
        + inp.carbs_g * KCAL_PER_G["carbs"]
    )
    if total_kcal <= 0:
        return 0
    actual = {
        "protein": inp.protein_g * KCAL_PER_G["protein"] / total_kcal,
        "fat": inp.fat_g * KCAL_PER_G["fat"] / total_kcal,
        "carbs": inp.carbs_g * KCAL_PER_G["carbs"] / total_kcal,
    }
    # 各マクロの乖離（絶対値）合計: 0 → 100点, 0.6以上 → 0点
    deviation = sum(abs(actual[k] - PFC_TARGET[k]) for k in PFC_TARGET)
    return max(0, min(100, round(100 * (1 - deviation / 0.6))))


def energy_balance_score(balance_kcal: float) -> int:
    """収支スコア。理想欠損(−300±200)で満点、極端な欠損/過剰で減点。"""
    deviation = abs(balance_kcal - IDEAL_DEFICIT_KCAL)
    if deviation <= DEFICIT_TOLERANCE:
        return 100
    # 許容から1000kcal逸脱でゼロ
    return max(0, round(100 * (1 - (deviation - DEFICIT_TOLERANCE) / 1000)))


def evaluate(inp: NutritionInput, effect_ttl_hours: int = 24) -> ConditionResult:
    """日次の食事+活動データ → コンディションスコアとBuff/Debuffリスト。"""
    balance = inp.calories_in - (inp.bmr_kcal + inp.active_calories)
    p_score = pfc_score(inp)
    e_score = energy_balance_score(balance)
    condition = round(0.55 * e_score + 0.45 * p_score)

    expires = (datetime.now(timezone.utc) + timedelta(hours=effect_ttl_hours)).isoformat()
    effects: list[dict] = []
    notes: list[str] = []

    def add(kind: str, code: str, mult: float, note: str) -> None:
        effects.append({
            "kind": kind, "code": code, "exp_multiplier": mult,
            "expires_at": expires, "granted_by": "nutrition_engine",
        })
        notes.append(note)

    # --- Buffs ---
    if inp.weight_kg > 0 and inp.protein_g / inp.weight_kg >= PROTEIN_BOOST_G_PER_KG:
        add("buff", "protein_boost", 1.10,
            f"タンパク質 {inp.protein_g / inp.weight_kg:.1f}g/kg 達成。回復力アップ（EXP+10%）")
    if e_score >= 90 and p_score >= 70:
        add("buff", "well_fueled", 1.05, "収支・PFCともに良好。モンスター絶好調（EXP+5%）")

    # --- Debuffs ---
    if balance <= SEVERE_DEFICIT_KCAL:
        add("debuff", "underfueled", 0.70,
            f"欠損 {balance:.0f}kcal は過大。回復不足で成長効率低下（EXP−30%）。食事量を戻そう")
    elif balance >= SURPLUS_LIMIT_KCAL:
        add("debuff", "overfed", 0.90,
            f"収支 +{balance:.0f}kcal。モンスターが重い（EXP−10%）")

    total_kcal = max(inp.calories_in, 1)
    if (inp.carbs_g * KCAL_PER_G["carbs"]) / total_kcal > SUGAR_CRASH_CARB_RATIO:
        add("debuff", "sugar_crash", 0.90, "炭水化物過多。夕方の眠気に注意（EXP−10%）")

    return ConditionResult(
        condition_score=condition,
        energy_balance_kcal=round(balance, 1),
        pfc_score=p_score,
        effects=effects,
        coaching_notes=notes,
    )


def combined_multiplier(effects: list[dict]) -> float:
    """アクティブな全効果の乗算合成（0.5–1.5にクランプ）。Growth Engineに渡す。"""
    mult = 1.0
    for e in effects:
        mult *= float(e.get("exp_multiplier", 1.0))
    return round(min(max(mult, 0.5), 1.5), 4)


def condition_to_animation(condition_score: int) -> str:
    """コンディション → フロントのアニメーション状態。"""
    if condition_score >= 80:
        return "happy"
    if condition_score >= 50:
        return "idle"
    if condition_score >= 30:
        return "tired"
    return "sick"
