"""Google Health Connect (モバイル送信) → NormalizedActivity。

Androidアプリが ExerciseSessionRecord / StepsRecord / HeartRateRecord /
ExerciseRouteRecord を HealthConnectSessionPayload に整形して送る。
"""

from typing import Any

from app.ingestion.base import ActivityNormalizer, downsample
from app.schemas.activity import HealthConnectSessionPayload, NormalizedActivity


class GoogleHealthConnectNormalizer(ActivityNormalizer):
    source = "google_health_connect"

    def normalize(self, payload: dict[str, Any]) -> list[NormalizedActivity]:
        user_id: str = payload["user_id"]  # JWT検証済みの内部ユーザーID
        out: list[NormalizedActivity] = []
        for raw in payload.get("health_connect_sessions", []):
            s = HealthConnectSessionPayload.model_validate(raw)
            duration = int((s.end_time - s.start_time).total_seconds())
            if duration <= 0:
                continue
            out.append(
                NormalizedActivity(
                    source="google_health_connect",
                    external_id=s.record_id,
                    provider_user_id=user_id,
                    activity_type=s.activity_type(),
                    started_at=s.start_time,
                    ended_at=s.end_time,
                    duration_s=duration,
                    distance_m=s.distance_m or 0,
                    steps=s.steps,
                    calories_active=s.active_calories_kcal,
                    hr_avg=self._avg_bpm(s),
                    hr_max=max((x.bpm for x in s.heart_rate_samples), default=None),
                    hr_samples=downsample(s.heart_rate_samples),
                    gps_samples=downsample(s.exercise_route),
                )
            )
        return out

    @staticmethod
    def _avg_bpm(s: HealthConnectSessionPayload) -> int | None:
        if not s.heart_rate_samples:
            return None
        return round(sum(x.bpm for x in s.heart_rate_samples) / len(s.heart_rate_samples))
