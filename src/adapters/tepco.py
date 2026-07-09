from __future__ import annotations

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter
from src.utils.http import get


class TepcoAdapter(BaseAdapter):
    source_id = "tepco"
    display_name = "TEPCO power demand"
    rank = "A"
    candidate_url = "https://www.tepco.co.jp/forecast/html/images/juyo-d1-j.csv"

    def probe(self) -> dict:
        response, sample = get(self.candidate_url, timeout=20)
        ok = response is not None and response.status_code == 200 and "csv" in (sample.content_type or sample.text_head[:100].lower())
        report = {
            "source_id": self.source_id,
            "status": "ok" if ok else "skip",
            "candidate_url": self.candidate_url,
            "sample_http": sample.as_dict(),
            "reason": "Candidate CSV endpoint checked; historical archive support is not assumed.",
        }
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict) -> FeatureRows:
        raise SkipAdapter("TEPCO historical CSV endpoint is not configured; probe only records current candidate response")
