"""Normalizer 抽象基底。各ソースのペイロード → NormalizedActivity 変換を担う。"""

from abc import ABC, abstractmethod
from typing import Any

from app.schemas.activity import GPSSample, HRSample, NormalizedActivity

MAX_SAMPLES = 720  # 保存するサンプル上限（1時間 @5s）。超過分は等間隔で間引く


def downsample(samples: list, limit: int = MAX_SAMPLES) -> list:
    if len(samples) <= limit:
        return samples
    step = len(samples) / limit
    return [samples[int(i * step)] for i in range(limit)]


class ActivityNormalizer(ABC):
    """1ソース分の生ペイロードを共通スキーマへ正規化する。

    実装規約:
    - 変換不能なフィールドは None にして落とさない（部分データでも受理し、
      欠損はアンチチート/成長エンジン側で扱う）
    - external_id は必ずソース側の永続IDを使う（リプレイ耐性）
    - hr/gps サンプルは downsample() で上限を保証する
    """

    source: str

    @abstractmethod
    def normalize(self, payload: dict[str, Any]) -> list[NormalizedActivity]:
        """生ペイロード（Webhook 1回分/同期1バッチ分）→ 正規化活動のリスト。"""

    @staticmethod
    def _hr(samples: list[dict], t_key: str, v_key: str) -> list[HRSample]:
        out = []
        for s in samples:
            t, v = s.get(t_key), s.get(v_key)
            if t is not None and v and 25 <= v <= 250:
                out.append(HRSample(t=int(t), bpm=int(v)))
        return downsample(out)

    @staticmethod
    def _gps(samples: list[dict], keys: dict[str, str]) -> list[GPSSample]:
        out = []
        for s in samples:
            lat, lng = s.get(keys["lat"]), s.get(keys["lng"])
            if lat is None or lng is None:
                continue
            out.append(
                GPSSample(
                    t=int(s.get(keys["t"], 0)),
                    lat=lat,
                    lng=lng,
                    alt=s.get(keys.get("alt", "")),
                    h_acc_m=s.get(keys.get("acc", "")),
                )
            )
        return downsample(out)
