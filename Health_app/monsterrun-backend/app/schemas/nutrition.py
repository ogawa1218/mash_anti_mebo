"""栄養ログの入出力スキーマ。"""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


class MealEntry(BaseModel):
    name: str
    time: datetime | None = None
    kcal: float = Field(ge=0)
    protein_g: float = Field(default=0, ge=0)
    fat_g: float = Field(default=0, ge=0)
    carbs_g: float = Field(default=0, ge=0)


class NutritionLogIn(BaseModel):
    """POST /v1/nutrition/logs — MyFitnessPal互換アダプタ/手入力の共通受け口。"""

    log_date: date
    source: Literal["myfitnesspal", "cronometer", "manual"] = "manual"
    meals: list[MealEntry]

    @property
    def totals(self) -> dict[str, float]:
        return {
            "calories_in": sum(m.kcal for m in self.meals),
            "protein_g": sum(m.protein_g for m in self.meals),
            "fat_g": sum(m.fat_g for m in self.meals),
            "carbs_g": sum(m.carbs_g for m in self.meals),
        }


class ConditionResult(BaseModel):
    """栄養エンジンの出力。"""

    condition_score: int = Field(ge=0, le=100)
    energy_balance_kcal: float
    pfc_score: int = Field(ge=0, le=100)
    effects: list[dict] = Field(default_factory=list)
    coaching_notes: list[str] = Field(default_factory=list)
