from __future__ import annotations

from datetime import datetime, timedelta

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter
from src.utils.http import get, json_or_none


class GbifAdapter(BaseAdapter):
    source_id = "gbif"
    display_name = "GBIF Occurrence API"
    rank = "A"
    url = "https://api.gbif.org/v1/occurrence/search"

    def probe(self) -> dict:
        response, sample = get(self.url, params={"country": "JP", "limit": 0}, timeout=20)
        data = json_or_none(response)
        report = {
            "source_id": self.source_id,
            "status": "ok" if isinstance(data, dict) and "count" in data else "error",
            "sample_http": sample.as_dict(),
            "sample_keys": list(data.keys()) if isinstance(data, dict) else [],
            "feature": "daily occurrence count by eventDate",
        }
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict) -> FeatureRows:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        if (end - start).days > 45:
            raise SkipAdapter("GBIF daily aggregation is capped at 45 days in the MVP to avoid excessive API calls")
        rows: FeatureRows = []
        day = start
        while day <= end:
            ds = day.date().isoformat()
            response, sample = get(self.url, params={"country": "JP", "eventDate": ds, "limit": 0}, timeout=20)
            data = json_or_none(response)
            if isinstance(data, dict) and "count" in data:
                rows.append({"date": ds, "source_id": self.source_id, "feature_name": "gbif_occurrences", "value": float(data["count"])})
            else:
                self.failure(status="fetch_error", date=ds, sample_http=sample.as_dict())
            day += timedelta(days=1)
        if not rows:
            raise SkipAdapter("No GBIF rows fetched")
        return rows
