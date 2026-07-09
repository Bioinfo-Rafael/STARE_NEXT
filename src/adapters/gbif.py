from __future__ import annotations

import re

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter
from src.utils.http import get, json_or_none


class GbifAdapter(BaseAdapter):
    source_id = "gbif"
    display_name = "GBIF Occurrence API"
    rank = "A"
    url = "https://api.gbif.org/v1/occurrence/search"

    def probe(self) -> dict:
        response, sample = get(self.url, params={"country": "JP", "eventDate": "2020-01-01,2020-01-07", "limit": 0, "facet": "eventDate", "facetLimit": 10}, timeout=20)
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
        response, sample = get(
            self.url,
            params={"country": "JP", "eventDate": f"{start_date},{end_date}", "limit": 0, "facet": "eventDate", "facetLimit": 2500},
            timeout=60,
        )
        data = json_or_none(response)
        if not isinstance(data, dict) or not isinstance(data.get("facets"), list):
            raise SkipAdapter(f"GBIF facet request did not return facets: {sample.error or sample.status_code}")
        rows: FeatureRows = []
        for facet in data.get("facets", []):
            if facet.get("field") not in {"eventDate", "eventDateInterval"}:
                continue
            for item in facet.get("counts", []):
                name = str(item.get("name", ""))
                if re.fullmatch(r"\d{4}-\d{2}-\d{2}", name):
                    rows.append({"date": name, "source_id": self.source_id, "feature_name": "gbif_occurrences", "value": float(item.get("count") or 0)})
        if not rows:
            raise SkipAdapter("No GBIF rows fetched")
        return rows
