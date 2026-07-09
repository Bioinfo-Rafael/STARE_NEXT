from __future__ import annotations

import os
import time

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter
from src.utils.http import get, json_or_none


class GdeltAdapter(BaseAdapter):
    source_id = "gdelt"
    display_name = "GDELT DOC 2.1 Timeline"
    rank = "S"
    queries = [
        "earthquake cloud",
        "animal strange behavior",
        "unusual animal behavior",
        "well water",
        "groundwater anomaly",
        "radio interference",
        "fish beaching",
        "地震雲",
        "動物 異常",
        "井戸水",
        "電波障害",
        "地鳴り",
        "異臭",
    ]

    def _params(self, query: str, start_date: str, end_date: str) -> dict[str, str]:
        return {
            "query": query,
            "mode": "timelinevol",
            "format": "json",
            "startdatetime": start_date.replace("-", "") + "000000",
            "enddatetime": end_date.replace("-", "") + "235959",
        }

    def probe(self) -> dict:
        url = "https://api.gdeltproject.org/api/v2/doc/doc"
        response, sample = get(url, params=self._params("earthquake", "2022-01-01", "2022-01-07"), timeout=int(os.getenv("GDELT_TIMEOUT_SECONDS", "12")))
        data = json_or_none(response)
        timeline = data.get("timeline", []) if isinstance(data, dict) else []
        status = "ok" if timeline else "error"
        if response is not None and response.status_code == 429:
            status = "rate_limited"
        report = {
            "source_id": self.source_id,
            "status": status,
            "sample_http": sample.as_dict(),
            "top_level_keys": list(data.keys()) if isinstance(data, dict) else [],
            "sample_row": timeline[0] if timeline else None,
            "time_grain": "timeline bucket, usually daily",
            "geo_grain": "query/global",
        }
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict) -> FeatureRows:
        rows: FeatureRows = []
        url = "https://api.gdeltproject.org/api/v2/doc/doc"
        max_queries = int(os.getenv("GDELT_MAX_QUERIES", "4"))
        timeout = int(os.getenv("GDELT_TIMEOUT_SECONDS", "12"))
        sleep_seconds = float(os.getenv("GDELT_SLEEP_SECONDS", "5.2"))
        for i, query in enumerate(self.queries[:max_queries]):
            if i:
                time.sleep(sleep_seconds)
            response, sample = get(url, params=self._params(query, start_date, end_date), timeout=timeout)
            if response is not None and response.status_code == 429:
                self.failure(status="rate_limited", query=query, sample_http=sample.as_dict())
                break
            data = json_or_none(response)
            if response is None or response.status_code != 200 or not isinstance(data, dict):
                self.failure(status="fetch_error", query=query, sample_http=sample.as_dict())
                continue
            timeline = data.get("timeline") or data.get("timelinevol") or []
            if not isinstance(timeline, list):
                self.failure(status="unexpected_schema", query=query, keys=list(data.keys()), sample_http=sample.as_dict())
                continue
            for item in timeline:
                dt = str(item.get("date") or item.get("datetime") or item.get("time") or "")
                date = dt[:10] if "-" in dt else f"{dt[:4]}-{dt[4:6]}-{dt[6:8]}" if len(dt) >= 8 else ""
                value = item.get("value", item.get("count", item.get("norm", 0)))
                try:
                    value = float(value)
                except Exception:
                    value = 0.0
                if date:
                    rows.append({"date": date, "source_id": self.source_id, "feature_name": f"gdelt_{query}", "value": value, "query": query})
        if not rows:
            raise SkipAdapter("No GDELT rows fetched; API may have timed out or returned a new schema")
        return rows
