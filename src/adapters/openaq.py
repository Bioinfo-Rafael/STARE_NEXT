from __future__ import annotations

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter
from src.utils.http import get, json_or_none


class OpenAqAdapter(BaseAdapter):
    source_id = "openaq"
    display_name = "OpenAQ"
    rank = "A"
    url = "https://api.openaq.org/v3/measurements"

    def probe(self) -> dict:
        response, sample = get(
            self.url,
            params={"coordinates": "35.681,139.767", "radius": 50000, "limit": 1},
            timeout=20,
        )
        data = json_or_none(response)
        status = "ok" if isinstance(data, dict) and response is not None and response.status_code == 200 else "skip"
        report = {
            "source_id": self.source_id,
            "status": status,
            "sample_http": sample.as_dict(),
            "sample_keys": list(data.keys()) if isinstance(data, dict) else [],
            "reason": "OpenAQ v3 may require an API key or different query parameters depending on deployment.",
        }
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict) -> FeatureRows:
        raise SkipAdapter("OpenAQ adapter currently probes schema only; add API key-aware pagination before full fetch")
