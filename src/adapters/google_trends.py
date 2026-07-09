from __future__ import annotations

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter


class GoogleTrendsAdapter(BaseAdapter):
    source_id = "google_trends"
    display_name = "Google Trends"
    rank = "S"
    terms = ["地震雲", "耳鳴り", "ペット おかしい", "井戸水", "電波障害", "地鳴り", "ナマズ", "防災グッズ", "南海トラフ", "地震 予兆", "揺れた", "地震速報"]

    def probe(self) -> dict:
        try:
            import pytrends  # type: ignore  # noqa: F401
            status = "available"
            reason = "pytrends import succeeded"
        except Exception as exc:
            status = "skip"
            reason = f"pytrends is unavailable or blocked: {exc!r}"
        report = {"source_id": self.source_id, "status": status, "reason": reason, "terms": self.terms}
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict) -> FeatureRows:
        try:
            from pytrends.request import TrendReq  # type: ignore
        except Exception as exc:
            raise SkipAdapter(f"pytrends not installed: {exc}")
        pytrends = TrendReq(hl="ja-JP", tz=540, retries=1, backoff_factor=0.2)
        rows: FeatureRows = []
        timeframe = f"{start_date} {end_date}"
        for term in self.terms:
            pytrends.build_payload([term], cat=0, timeframe=timeframe, geo="JP", gprop="")
            df = pytrends.interest_over_time()
            if df is None or df.empty:
                continue
            for idx, rec in df.iterrows():
                rows.append({"date": idx.date().isoformat(), "source_id": self.source_id, "feature_name": f"trend_{term}", "value": float(rec.get(term, 0))})
        if not rows:
            raise SkipAdapter("Google Trends returned no rows")
        return rows
