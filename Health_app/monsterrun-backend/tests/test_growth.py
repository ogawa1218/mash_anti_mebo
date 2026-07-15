"""成長エンジン・進化分岐・栄養エンジンの数理テスト。"""

from app.engine.evolution import (
    decide_branch,
    evolution_points,
    zone_seconds_from_samples,
)
from app.engine.growth import (
    ExpInput,
    apply_exp_to_level,
    calc_exp,
    exp_required_for_level,
    novice_bonus,
    temperature_correction,
)
from app.engine.nutrition import NutritionInput, evaluate
from app.schemas.activity import HRSample


def _exp(distance_km, hr_avg, hr_rest, lifetime_km=0.0, temp=None):
    return calc_exp(ExpInput(
        distance_km=distance_km, hr_avg=hr_avg, hr_rest=hr_rest,
        temperature_c=temp, lifetime_distance_km=lifetime_km,
    ))


class TestExpFormula:
    def test_basic_formula(self):
        # EXP = 5 × (150/60) × 1.0 × 10 × 1.5(novice) = 187.5
        r = _exp(5.0, 150, 60, lifetime_km=0)
        assert r.exp == 187.5

    def test_beginner_beats_veteran_at_same_pace(self):
        """同じ5km・同じ安静時心拍でも、心拍が上がりやすい初心者の方が多くEXPを得る。"""
        beginner = _exp(5.0, 170, 65, lifetime_km=20)    # 初心者: 心拍170まで上がる
        veteran = _exp(5.0, 125, 65, lifetime_km=3000)   # 上級者: 楽に125で走れる
        assert beginner.exp > veteran.exp * 1.5

    def test_hr_ratio_is_capped(self):
        r = _exp(5.0, 240, 40)  # 比率6.0 → 3.5にクリップ
        assert r.hr_ratio == 3.5

    def test_novice_bonus_decays(self):
        assert novice_bonus(0) == 1.5
        assert 1.0 < novice_bonus(1000) < 1.05
        assert novice_bonus(0) > novice_bonus(100) > novice_bonus(500)

    def test_temperature_correction(self):
        assert temperature_correction(15) == 1.0       # 快適域
        assert temperature_correction(None) == 1.0
        assert 1.0 < temperature_correction(30) <= 1.15  # 暑熱
        assert 1.0 < temperature_correction(0) <= 1.15   # 寒冷
        assert temperature_correction(45) == 1.15        # 上限

    def test_missing_hr_uses_conservative_ratio(self):
        assert _exp(5.0, None, 60).hr_ratio == 1.4


class TestLevelCurve:
    def test_exp_required_increases(self):
        assert exp_required_for_level(1) == 100.0
        assert exp_required_for_level(10) > exp_required_for_level(5)

    def test_multi_level_up_with_carryover(self):
        level, leftover = apply_exp_to_level(1, 0, 250)  # 100 + 115 = 215 消費
        assert level == 3
        assert leftover == 35.0

    def test_level_cap(self):
        level, _ = apply_exp_to_level(100, 0, 10**9)
        assert level == 100


class TestEvolution:
    def test_lsd_accumulates_stamina(self):
        # 60分すべてZ2（HRR 60-70%）: hr_rest=60, hr_max=180 → 132-144bpm
        samples = [HRSample(t=i * 60, bpm=138) for i in range(60)]
        zones = zone_seconds_from_samples(samples, hr_rest=60, hr_max=180)
        delta = evolution_points(zones)
        assert delta.stamina_points > 0
        assert delta.speed_points == 0

    def test_hiit_accumulates_speed(self):
        # HRR 90%超（168bpm〜）を維持
        samples = [HRSample(t=i * 30, bpm=172) for i in range(40)]
        zones = zone_seconds_from_samples(samples, hr_rest=60, hr_max=180)
        delta = evolution_points(zones)
        assert delta.speed_points > 0
        assert delta.stamina_points == 0

    def test_branch_decision(self):
        assert decide_branch(1000, 100) == "stamina_guardian"
        assert decide_branch(100, 1000) == "speed_striker"
        assert decide_branch(500, 520) == "balanced"


class TestNutrition:
    def _input(self, kcal_in, p=120, f=50, c=180, active=400):
        return NutritionInput(
            calories_in=kcal_in, protein_g=p, fat_g=f, carbs_g=c,
            active_calories=active, bmr_kcal=1600, weight_kg=70,
        )

    def test_ideal_deficit_gives_high_condition(self):
        # 収支 = 1700 - (1600+400) = -300 → 理想
        r = evaluate(self._input(1700))
        assert r.condition_score >= 80
        assert r.energy_balance_kcal == -300.0

    def test_severe_deficit_triggers_underfueled_debuff(self):
        r = evaluate(self._input(900))  # 収支 -1100
        codes = [e["code"] for e in r.effects]
        assert "underfueled" in codes
        assert any(e["exp_multiplier"] < 1.0 for e in r.effects if e["code"] == "underfueled")

    def test_high_protein_grants_buff(self):
        r = evaluate(self._input(1700, p=120))  # 120g/70kg = 1.71g/kg
        assert "protein_boost" in [e["code"] for e in r.effects]

    def test_carb_overload_triggers_sugar_crash(self):
        r = evaluate(self._input(2000, p=30, f=20, c=350))
        assert "sugar_crash" in [e["code"] for e in r.effects]
