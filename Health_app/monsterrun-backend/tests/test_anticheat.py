"""アンチチートエンジンのヒューリスティック検証。"""

from datetime import datetime, timedelta, timezone

from app.engine.anticheat import AntiCheatEngine
from app.schemas.activity import GPSSample, HRSample, NormalizedActivity

engine = AntiCheatEngine()
T0 = datetime(2026, 7, 1, 6, 0, tzinfo=timezone.utc)
EPOCH0 = int(T0.timestamp())


def _activity(duration_s=1800, distance_m=5000, hr_avg=150, steps=None,
              gps=None, hr_samples=None, activity_type="run") -> NormalizedActivity:
    return NormalizedActivity(
        source="apple_healthkit", external_id="test-1", provider_user_id="u1",
        activity_type=activity_type,
        started_at=T0, ended_at=T0 + timedelta(seconds=duration_s),
        duration_s=duration_s, distance_m=distance_m,
        hr_avg=hr_avg, steps=steps,
        gps_samples=gps or [], hr_samples=hr_samples or [],
    )


def _track(speed_kmh: float, n_points: int = 60, interval_s: int = 10) -> list[GPSSample]:
    """一定速度で北進するGPS軌跡。緯度1度 ≈ 111.32km。"""
    deg_per_s = speed_kmh / 3600 / 111.32
    return [
        GPSSample(t=EPOCH0 + i * interval_s, lat=35.0 + deg_per_s * i * interval_s, lng=139.0)
        for i in range(n_points)
    ]


class TestH1ImpossibleSpeed:
    def test_train_speed_quarantined(self):
        """時速40kmで30分「走った」→ 乗り物判定。"""
        act = _activity(duration_s=1800, distance_m=20000, hr_avg=150, gps=_track(40.0))
        v = engine.evaluate(act, hr_rest=60)
        assert any(f.code == "H1_IMPOSSIBLE_SPEED" for f in v.flags)

    def test_fast_but_human_pace_ok(self):
        """キロ4分(15km/h)は人間の速度。H1は発火しない。"""
        act = _activity(duration_s=1200, distance_m=5000, hr_avg=165, gps=_track(15.0, n_points=120))
        v = engine.evaluate(act, hr_rest=60)
        assert not any(f.code == "H1_IMPOSSIBLE_SPEED" for f in v.flags)

    def test_no_gps_fallback_uses_average(self):
        act = _activity(duration_s=1800, distance_m=15000, hr_avg=150)  # 平均30km/h・GPSなし
        v = engine.evaluate(act, hr_rest=60)
        assert any(f.code == "H1_IMPOSSIBLE_SPEED" for f in v.flags)


class TestH2HrSpeedMismatch:
    def test_resting_hr_at_15kmh_is_vehicle(self):
        """時速16kmで移動中に心拍68bpm（安静時60）→ 自動車・自転車移動。"""
        act = _activity(duration_s=1800, distance_m=8000, hr_avg=68)
        v = engine.evaluate(act, hr_rest=60)
        assert any(f.code == "H2_HR_SPEED_MISMATCH" for f in v.flags)

    def test_elevated_hr_at_15kmh_is_legit(self):
        act = _activity(duration_s=1800, distance_m=8000, hr_avg=162)
        v = engine.evaluate(act, hr_rest=60)
        assert not any(f.code == "H2_HR_SPEED_MISMATCH" for f in v.flags)

    def test_ride_activity_exempt(self):
        act = _activity(duration_s=1800, distance_m=12000, hr_avg=70, activity_type="ride")
        v = engine.evaluate(act, hr_rest=60)
        assert not any(f.code == "H2_HR_SPEED_MISMATCH" for f in v.flags)


class TestH3StrideAnomaly:
    def test_tiny_stride_flags_shaker(self):
        """5000歩で500m → 歩幅0.1m。シェイカーで歩数だけ稼いだパターン。"""
        act = _activity(duration_s=3600, distance_m=500, hr_avg=80, steps=5000)
        v = engine.evaluate(act, hr_rest=60)
        assert any(f.code == "H3_STRIDE_ANOMALY" for f in v.flags)

    def test_giant_stride_flags_gps_spoof(self):
        """1000歩で5000m → 歩幅5m。距離偽装。"""
        act = _activity(duration_s=1800, distance_m=5000, hr_avg=150, steps=1000)
        v = engine.evaluate(act, hr_rest=60)
        assert any(f.code == "H3_STRIDE_ANOMALY" for f in v.flags)

    def test_normal_stride_ok(self):
        act = _activity(duration_s=1800, distance_m=5000, hr_avg=150, steps=4500)  # 1.11m
        v = engine.evaluate(act, hr_rest=60)
        assert not any(f.code == "H3_STRIDE_ANOMALY" for f in v.flags)


class TestH4Shaker:
    def test_steps_without_displacement_flat_hr(self):
        """歩数6000・GPSほぼ静止・心拍平坦 → シェイカー。"""
        static_gps = [GPSSample(t=EPOCH0 + i * 30, lat=35.0, lng=139.0) for i in range(30)]
        flat_hr = [HRSample(t=EPOCH0 + i * 30, bpm=62) for i in range(30)]
        act = _activity(duration_s=900, distance_m=4200, hr_avg=62,
                        steps=6000, gps=static_gps, hr_samples=flat_hr)
        v = engine.evaluate(act, hr_rest=60)
        assert any(f.code == "H4_SHAKER_PATTERN" for f in v.flags)
        assert v.status == "quarantined"  # H2/H3/H4が重なり score >= 50

    def test_real_walk_not_flagged(self):
        gps = _track(5.0, n_points=60, interval_s=30)
        hr = [HRSample(t=EPOCH0 + i * 30, bpm=95 + (i % 20)) for i in range(60)]
        act = _activity(duration_s=1800, distance_m=2500, hr_avg=105,
                        steps=3300, gps=gps, hr_samples=hr, activity_type="walk")
        v = engine.evaluate(act, hr_rest=60)
        assert v.status == "accepted"


class TestH5GpsTeleport:
    def test_teleport_spikes_flagged(self):
        gps = _track(10.0, n_points=30)
        # 2点を大きくジャンプさせる（座標偽装アプリの切替に相当）
        gps[10] = GPSSample(t=gps[10].t, lat=35.5, lng=139.0)
        gps[20] = GPSSample(t=gps[20].t, lat=34.5, lng=139.0)
        act = _activity(duration_s=300, distance_m=1000, hr_avg=150, gps=gps)
        v = engine.evaluate(act, hr_rest=60)
        assert any(f.code == "H5_GPS_TELEPORT" for f in v.flags)


class TestVerdictThresholds:
    def test_clean_run_accepted(self):
        gps = _track(10.0, n_points=180)
        hr = [HRSample(t=EPOCH0 + i * 10, bpm=145 + (i % 15)) for i in range(180)]
        act = _activity(duration_s=1800, distance_m=5000, hr_avg=152,
                        steps=4600, gps=gps, hr_samples=hr)
        v = engine.evaluate(act, hr_rest=60)
        assert v.status == "accepted"
        assert v.score == 0

    def test_score_is_capped_at_100(self):
        act = _activity(duration_s=1800, distance_m=20000, hr_avg=65, steps=100000,
                        gps=_track(40.0))
        v = engine.evaluate(act, hr_rest=60)
        assert v.score <= 100
        assert v.status == "quarantined"
