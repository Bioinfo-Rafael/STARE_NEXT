from __future__ import annotations

import os
import json
import hashlib
import time

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter
from src.utils.http import get, json_or_none
from src.utils.io import ensure_dir


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

    def _year_windows(self, start_date: str, end_date: str) -> list[tuple[str, str]]:
        start_year = int(start_date[:4])
        end_year = int(end_date[:4])
        windows: list[tuple[str, str]] = []
        for year in range(start_year, end_year + 1):
            y_start = max(start_date, f"{year}-01-01")
            y_end = min(end_date, f"{year}-12-31")
            windows.append((y_start, y_end))
        return windows

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
        max_queries = int(os.getenv("GDELT_MAX_QUERIES", "1"))
        timeout = int(os.getenv("GDELT_TIMEOUT_SECONDS", "5"))
        sleep_seconds = float(os.getenv("GDELT_SLEEP_SECONDS", "5.2"))
        retries = int(os.getenv("GDELT_RETRIES", "0"))
        cache_dir = ensure_dir(self.output_dir / "metadata" / "gdelt_cache")
        request_count = 0
        rate_limited = False
        for query in self.queries[:max_queries]:
            for window_start, window_end in self._year_windows(start_date, end_date):
                params = self._params(query, window_start, window_end)
                cache_key = hashlib.sha256(json.dumps(params, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:24]
                cache_path = cache_dir / f"{cache_key}.json"
                sample = None
                if cache_path.exists():
                    data = json.loads(cache_path.read_text(encoding="utf-8"))
                else:
                    data = None
                    for attempt in range(retries + 1):
                        if request_count or attempt:
                            time.sleep(sleep_seconds)
                        request_count += 1
                        response, sample = get(url, params=params, timeout=timeout)
                        if response is not None and response.status_code == 429:
                            rate_limited = True
                            self.failure(status="rate_limited_retry", query=query, start_date=window_start, attempt=attempt, sample_http=sample.as_dict())
                            continue
                        data = json_or_none(response)
                        if response is not None and response.status_code == 200 and isinstance(data, dict):
                            cache_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
                            break
                        self.failure(status="fetch_error", query=query, start_date=window_start, attempt=attempt, sample_http=sample.as_dict())
                    if not isinstance(data, dict):
                        continue
                timeline = data.get("timeline") or data.get("timelinevol") or []
                if not isinstance(timeline, list):
                    self.failure(status="unexpected_schema", query=query, keys=list(data.keys()), sample_http=sample.as_dict() if sample else None)
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
            reason = "GDELT stayed rate-limited after yearly split sleep/retry" if rate_limited else "No GDELT rows fetched; API may have timed out or returned a new schema"
            raise SkipAdapter(reason)
        return rows
