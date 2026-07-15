"""正規化アクティビティスキーマと、モバイル(HealthKit/Health Connect)送信ペイロード定義。

全ソースは最終的に NormalizedActivity へ変換される。これが
Anti-Cheat → Growth Engine → DB永続化 の唯一の入力フォーマット。
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class HRSample(BaseModel):
    t: int = Field(description="Unix epoch seconds")
    bpm: int = Field(ge=25, le=250)


class GPSSample(BaseModel):
    t: int = Field(description="Unix epoch seconds")
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    alt: float | None = None
    h_acc_m: float | None = Field(default=None, description="水平精度(m)。低精度点はアンチチートで減衰")


class NormalizedActivity(BaseModel):
    """全ウェアラブルソース共通の正規化アクティビティ。"""

    source: Literal["garmin", "strava", "apple_healthkit", "google_health_connect", "manual"]
    external_id: str = Field(description="ソース側の一意ID（冪等キーの一部）")
    provider_user_id: str = Field(description="ソース側ユーザー識別子 → wearable_connections で内部IDへ解決")
    activity_type: Literal["run", "walk", "ride", "swim", "strength", "hike", "other"] = "run"
    started_at: datetime
    ended_at: datetime
    duration_s: int = Field(gt=0)
    distance_m: float = Field(ge=0)
    steps: int | None = Field(default=None, ge=0)
    calories_active: float | None = Field(default=None, ge=0)
    hr_avg: int | None = Field(default=None, ge=25, le=250)
    hr_max: int | None = Field(default=None, ge=25, le=250)
    hr_samples: list[HRSample] = Field(default_factory=list)
    gps_samples: list[GPSSample] = Field(default_factory=list)
    elevation_gain_m: float | None = None
    temperature_c: float | None = None

    @model_validator(mode="after")
    def _sane_times(self) -> "NormalizedActivity":
        if self.ended_at <= self.started_at:
            raise ValueError("ended_at must be after started_at")
        # 申告duration と実時間の乖離が大きいデータは受理段階で弾く（±20%または60秒）
        wall = (self.ended_at - self.started_at).total_seconds()
        if self.duration_s > wall * 1.2 + 60:
            raise ValueError("duration_s exceeds wall-clock window")
        return self


# ---------------------------------------------------------------------------
# Apple HealthKit — iOSアプリが HKWorkout + 関連サンプルを整形して送信
# ---------------------------------------------------------------------------
class HealthKitWorkoutPayload(BaseModel):
    """POST /v1/sync/mobile (platform=apple_healthkit) の1ワークアウト分。

    iOS側の対応: HKWorkout(uuid, workoutActivityType, startDate, endDate),
    HKQuantityType: stepCount / activeEnergyBurned / heartRate / distanceWalkingRunning,
    CLLocation (HKWorkoutRoute) → gps
    """

    workout_uuid: str = Field(description="HKWorkout.uuid — 冪等キー")
    workout_activity_type: int = Field(description="HKWorkoutActivityType rawValue (37=running, 52=walking...)")
    start_date: datetime
    end_date: datetime
    duration_s: float
    total_distance_m: float | None = None
    active_energy_kcal: float | None = Field(default=None, description="HKQuantityTypeIdentifier.activeEnergyBurned 合計")
    step_count: int | None = Field(default=None, description="期間内 HKQuantityTypeIdentifier.stepCount 合計")
    heart_rate_samples: list[HRSample] = Field(default_factory=list, description="最大1Hz、クライアント側で5s間隔にダウンサンプル")
    route: list[GPSSample] = Field(default_factory=list, description="HKWorkoutRoute → CLLocation列。5s間隔")
    source_bundle_id: str | None = Field(default=None, description="記録アプリのbundle id（アンチチート補助信号）")
    device_model: str | None = None

    # HKWorkoutActivityType rawValue → 内部タイプ
    _TYPE_MAP = {37: "run", 52: "walk", 13: "ride", 46: "swim", 20: "strength", 24: "hike"}

    def activity_type(self) -> str:
        return self._TYPE_MAP.get(self.workout_activity_type, "other")


# ---------------------------------------------------------------------------
# Google Health Connect — AndroidアプリがExerciseSessionRecordを整形して送信
# ---------------------------------------------------------------------------
class HealthConnectSessionPayload(BaseModel):
    """POST /v1/sync/mobile (platform=google_health_connect) の1セッション分。

    Android側の対応: ExerciseSessionRecord, StepsRecord, ActiveCaloriesBurnedRecord,
    HeartRateRecord, ExerciseRouteRecord(またはLocationデータ)
    """

    record_id: str = Field(description="ExerciseSessionRecord.metadata.id — 冪等キー")
    exercise_type: int = Field(description="ExerciseSessionRecord.EXERCISE_TYPE_* 定数 (56=RUNNING, 79=WALKING...)")
    start_time: datetime
    end_time: datetime
    distance_m: float | None = None
    active_calories_kcal: float | None = None
    steps: int | None = None
    heart_rate_samples: list[HRSample] = Field(default_factory=list)
    exercise_route: list[GPSSample] = Field(default_factory=list)
    data_origin_package: str | None = Field(default=None, description="記録アプリのpackage名（アンチチート補助信号）")
    device_model: str | None = None

    _TYPE_MAP = {56: "run", 57: "run", 79: "walk", 8: "ride", 73: "swim", 70: "strength", 37: "hike"}

    def activity_type(self) -> str:
        return self._TYPE_MAP.get(self.exercise_type, "other")


class MobileSyncRequest(BaseModel):
    """モバイルアプリからのバッチ同期リクエスト。JWT認証必須。"""

    platform: Literal["apple_healthkit", "google_health_connect"]
    healthkit_workouts: list[HealthKitWorkoutPayload] = Field(default_factory=list)
    health_connect_sessions: list[HealthConnectSessionPayload] = Field(default_factory=list)
    client_version: str
    sent_at: datetime

    @model_validator(mode="after")
    def _platform_matches(self) -> "MobileSyncRequest":
        if self.platform == "apple_healthkit" and self.health_connect_sessions:
            raise ValueError("platform mismatch")
        if self.platform == "google_health_connect" and self.healthkit_workouts:
            raise ValueError("platform mismatch")
        return self
