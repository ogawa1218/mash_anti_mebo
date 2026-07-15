"""Strava Webhook → fetch-on-event → NormalizedActivity.

StravaのWebhookイベントは活動の中身を含まない:
  {"object_type": "activity", "object_id": 123, "aspect_type": "create",
   "owner_id": 9876, "subscription_id": 1, "event_time": 1700000000}

そのため本Normalizerは httpx で以下を取得してから正規化する:
  GET /api/v3/activities/{id}                       … サマリ
  GET /api/v3/activities/{id}/streams?keys=time,heartrate,latlng,altitude
"""

from datetime import datetime, timedelta
from typing import Any

import httpx

from app.ingestion.base import ActivityNormalizer, downsample
from app.schemas.activity import GPSSample, HRSample, NormalizedActivity

STRAVA_API = "https://www.strava.com/api/v3"

_STRAVA_TYPE_MAP = {
    "Run": "run", "TrailRun": "run", "VirtualRun": "run",
    "Walk": "walk", "Ride": "ride", "VirtualRide": "ride",
    "Swim": "swim", "WeightTraining": "strength", "Hike": "hike",
}


class StravaNormalizer(ActivityNormalizer):
    source = "strava"

    async def fetch_and_normalize(
        self, event: dict[str, Any], access_token: str
    ) -> list[NormalizedActivity]:
        """Webhookイベント + 復号済みアクセストークン → API取得 → 正規化。"""
        if event.get("object_type") != "activity" or event.get("aspect_type") == "delete":
            return []
        activity_id = event["object_id"]
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient(timeout=15) as client:
            detail = (await client.get(f"{STRAVA_API}/activities/{activity_id}", headers=headers)).json()
            streams_resp = await client.get(
                f"{STRAVA_API}/activities/{activity_id}/streams",
                params={"keys": "time,heartrate,latlng,altitude", "key_by_type": "true"},
                headers=headers,
            )
            streams = streams_resp.json() if streams_resp.status_code == 200 else {}

        return self.normalize({"detail": detail, "streams": streams, "owner_id": event["owner_id"]})

    def normalize(self, payload: dict[str, Any]) -> list[NormalizedActivity]:
        detail: dict = payload["detail"]
        streams: dict = payload.get("streams", {})
        start = datetime.fromisoformat(detail["start_date"].replace("Z", "+00:00"))
        duration = int(detail.get("elapsed_time") or detail.get("moving_time") or 0)
        if duration <= 0:
            return []
        start_epoch = int(start.timestamp())

        times = streams.get("time", {}).get("data", [])
        hrs = streams.get("heartrate", {}).get("data", [])
        latlngs = streams.get("latlng", {}).get("data", [])
        alts = streams.get("altitude", {}).get("data", [])

        hr_samples = downsample(
            [HRSample(t=start_epoch + t, bpm=bpm)
             for t, bpm in zip(times, hrs) if 25 <= bpm <= 250]
        )
        gps_samples = downsample(
            [GPSSample(t=start_epoch + t, lat=ll[0], lng=ll[1],
                       alt=alts[i] if i < len(alts) else None)
             for i, (t, ll) in enumerate(zip(times, latlngs)) if ll]
        )

        return [NormalizedActivity(
            source="strava",
            external_id=str(detail["id"]),
            provider_user_id=str(payload.get("owner_id") or detail.get("athlete", {}).get("id", "")),
            activity_type=_STRAVA_TYPE_MAP.get(detail.get("sport_type") or detail.get("type", ""), "other"),
            started_at=start,
            ended_at=start + timedelta(seconds=duration),
            duration_s=duration,
            distance_m=float(detail.get("distance") or 0),
            steps=None,  # Stravaは歩数を提供しない
            calories_active=detail.get("calories") or detail.get("kilojoules"),
            hr_avg=round(detail["average_heartrate"]) if detail.get("average_heartrate") else None,
            hr_max=round(detail["max_heartrate"]) if detail.get("max_heartrate") else None,
            hr_samples=hr_samples,
            gps_samples=gps_samples,
            elevation_gain_m=detail.get("total_elevation_gain"),
            temperature_c=detail.get("average_temp"),
        )]
