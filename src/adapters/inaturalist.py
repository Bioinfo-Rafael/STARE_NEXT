from __future__ import annotations

from datetime import datetime, timedelta

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter
from src.utils.http import get, json_or_none


class INaturalistAdapter(BaseAdapter):
    source_id = "inaturalist"
    display_name = "iNaturalist observations"
    rank = "A"
    url = "https://api.inaturalist.org/v1/observations"

    def _params(self, date: str | None = None) -> dict:
        params = {"nelat": 46, "nelng": 154, "swlat": 20, "swlng": 122, "per_page": 0}
        if date:
            params.update({"d1": date, "d2": date})
        return params

    def probe(self) -> dict:
        response, sample = get(self.url, params=self._params(), timeout=20)
        data = json_or_none(response)
        report = {
            "source_id": self.source_id,
            "status": "ok" if isinstance(data, dict) and "total_results" in data else "error",
            "sample_http": sample.as_dict(),
            "sample_keys": list(data.keys()) if isinstance(data, dict) else [],
            "geo_grain": "Japan bounding box",
            "feature": "daily observation count",
        }
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict) -> FeatureRows:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        if (end - start).days > 45:
            raise SkipAdapter("iNaturalist daily aggregation is capped at 45 days in the MVP to avoid excessive API calls")
        rows: FeatureRows = []
        day = start
        while day <= end:
            ds = day.date().isoformat()
            response, sample = get(self.url, params=self._params(ds), timeout=20)
            data = json_or_none(response)
            if isinstance(data, dict) and "total_results" in data:
                rows.append({"date": ds, "source_id": self.source_id, "feature_name": "inaturalist_observations", "value": float(data["total_results"])})
            else:
                self.failure(status="fetch_error", date=ds, sample_http=sample.as_dict())
            day += timedelta(days=1)
        if not rows:
            raise SkipAdapter("No iNaturalist rows fetched")
        return rows
