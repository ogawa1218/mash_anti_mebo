"""Apple HealthKit (モバイル送信) → NormalizedActivity。

iOSアプリが HKWorkout / HKQuantitySample / HKWorkoutRoute を
HealthKitWorkoutPayload に整形して POST /v1/sync/mobile へ送る。
provider_user_id には認証済みJWTの user_id がAPI層でセットされる
（モバイル経路は自己申告のため、アンチチートの重み付けが最も厳しい）。
"""

from typing import Any

from app.ingestion.base import ActivityNormalizer, downsample
from app.schemas.activity import HealthKitWorkoutPayload, NormalizedActivity


class AppleHealthKitNormalizer(ActivityNormalizer):
    source = "apple_healthkit"

    def normalize(self, payload: dict[str, Any]) -> list[NormalizedActivity]:
        user_id: str = payload["user_id"]  # JWT検証済みの内部ユーザーID
        out: list[NormalizedActivity] = []
        for raw in payload.get("healthkit_workouts", []):
            w = HealthKitWorkoutPayload.model_validate(raw)
            out.append(
                NormalizedActivity(
                    source="apple_healthkit",
                    external_id=w.workout_uuid,
                    provider_user_id=user_id,
                    activity_type=w.activity_type(),
                    started_at=w.start_date,
                    ended_at=w.end_date,
                    duration_s=int(w.duration_s),
                    distance_m=w.total_distance_m or 0,
                    steps=w.step_count,
                    calories_active=w.active_energy_kcal,
                    hr_avg=self._avg_bpm(w),
                    hr_max=max((s.bpm for s in w.heart_rate_samples), default=None),
                    hr_samples=downsample(w.heart_rate_samples),
                    gps_samples=downsample(w.route),
                )
            )
        return out

    @staticmethod
    def _avg_bpm(w: HealthKitWorkoutPayload) -> int | None:
        if not w.heart_rate_samples:
            return None
        return round(sum(s.bpm for s in w.heart_rate_samples) / len(w.heart_rate_samples))
