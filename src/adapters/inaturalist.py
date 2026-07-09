from __future__ import annotations

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter
from src.utils.http import get, json_or_none


class INaturalistAdapter(BaseAdapter):
    source_id = "inaturalist"
    display_name = "iNaturalist observations"
    rank = "A"
    url = "https://api.inaturalist.org/v1/observations"

    def _params(self, date: str | None = None) -> dict:
        params = {
            "nelat": 46,
            "nelng": 154,
            "swlat": 20,
            "swlng": 122,
            "date_field": "observed",
            "interval": "day",
        }
        if date:
            params.update({"d1": date, "d2": date})
        return params

    def probe(self) -> dict:
        response, sample = get("https://api.inaturalist.org/v1/observations/histogram", params=self._params("2020-01-01"), timeout=20)
        data = json_or_none(response)
        report = {
            "source_id": self.source_id,
            "status": "ok" if isinstance(data, dict) and isinstance(data.get("results"), dict) else "error",
            "sample_http": sample.as_dict(),
            "sample_keys": list(data.keys()) if isinstance(data, dict) else [],
            "geo_grain": "Japan bounding box",
            "feature": "daily observation count",
        }
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict) -> FeatureRows:
        response, sample = get(
            "https://api.inaturalist.org/v1/observations/histogram",
            params=self._params(None) | {"d1": start_date, "d2": end_date},
            timeout=60,
        )
        data = json_or_none(response)
        if not isinstance(data, dict) or not isinstance(data.get("results"), dict):
            raise SkipAdapter(f"iNaturalist histogram did not return daily results: {sample.error or sample.status_code}")
        rows: FeatureRows = []
        for date, count in sorted((data.get("results") or {}).get("day", {}).items()):
            rows.append({"date": date, "source_id": self.source_id, "feature_name": "inaturalist_observations", "value": float(count or 0)})
        if not rows:
            raise SkipAdapter("No iNaturalist rows fetched")
        return rows
