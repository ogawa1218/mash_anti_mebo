"""Garmin Connect Push API → NormalizedActivity.

Garmin Health API は登録済みWebhookへ activities / activityDetails をPushする。
activityDetails には samples（心拍・GPS・速度の時系列）が含まれる。

参考ペイロード構造（Health API "Activity Details Summaries"）:
{
  "activityDetails": [
    {
      "userId": "...", "userAccessToken": "...",
      "summaryId": "x123-detail",
      "summary": {
        "activityId": 123456,
        "activityType": "RUNNING",
        "startTimeInSeconds": 1700000000,
        "startTimeOffsetInSeconds": 32400,
        "durationInSeconds": 1800,
        "distanceInMeters": 5000.0,
        "activeKilocalories": 320,
        "averageHeartRateInBeatsPerMinute": 152,
        "maxHeartRateInBeatsPerMinute": 171,
        "steps": 5200,
        "totalElevationGainInMeters": 40.0
      },
      "samples": [
        {"startTimeInSeconds": 1700000000, "heartRate": 120,
         "latitudeInDegree": 35.68, "longitudeInDegree": 139.76,
         "elevationInMeters": 12.0}, ...
      ]
    }
  ]
}
"""

from datetime import datetime, timezone
from typing import Any

from app.ingestion.base import ActivityNormalizer
from app.schemas.activity import NormalizedActivity

_GARMIN_TYPE_MAP = {
    "RUNNING": "run",
    "INDOOR_RUNNING": "run",
    "TRAIL_RUNNING": "run",
    "TREADMILL_RUNNING": "run",
    "WALKING": "walk",
    "CYCLING": "ride",
    "INDOOR_CYCLING": "ride",
    "LAP_SWIMMING": "swim",
    "OPEN_WATER_SWIMMING": "swim",
    "STRENGTH_TRAINING": "strength",
    "HIKING": "hike",
}


class GarminNormalizer(ActivityNormalizer):
    source = "garmin"

    def normalize(self, payload: dict[str, Any]) -> list[NormalizedActivity]:
        items = payload.get("activityDetails") or payload.get("activities") or []
        return [a for item in items if (a := self._one(item)) is not None]

    def _one(self, item: dict[str, Any]) -> NormalizedActivity | None:
        summary = item.get("summary", item)
        start = summary.get("startTimeInSeconds")
        duration = summary.get("durationInSeconds")
        if start is None or not duration:
            return None

        started_at = datetime.fromtimestamp(start, tz=timezone.utc)
        ended_at = datetime.fromtimestamp(start + duration, tz=timezone.utc)
        samples = item.get("samples", [])

        return NormalizedActivity(
            source="garmin",
            external_id=str(summary.get("activityId") or item.get("summaryId")),
            provider_user_id=item.get("userAccessToken") or item.get("userId", ""),
            activity_type=_GARMIN_TYPE_MAP.get(summary.get("activityType", ""), "other"),
            started_at=started_at,
            ended_at=ended_at,
            duration_s=int(duration),
            distance_m=float(summary.get("distanceInMeters") or 0),
            steps=summary.get("steps"),
            calories_active=summary.get("activeKilocalories"),
            hr_avg=summary.get("averageHeartRateInBeatsPerMinute"),
            hr_max=summary.get("maxHeartRateInBeatsPerMinute"),
            hr_samples=self._hr(samples, "startTimeInSeconds", "heartRate"),
            gps_samples=self._gps(
                samples,
                {"t": "startTimeInSeconds", "lat": "latitudeInDegree",
                 "lng": "longitudeInDegree", "alt": "elevationInMeters"},
            ),
            elevation_gain_m=summary.get("totalElevationGainInMeters"),
            temperature_c=summary.get("airTemperatureCelcius"),
        )
