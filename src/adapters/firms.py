from __future__ import annotations

import csv
import io
import os
from collections import defaultdict
from datetime import datetime, timedelta

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter
from src.utils.http import get


class FirmsAdapter(BaseAdapter):
    source_id = "firms"
    display_name = "NASA FIRMS"
    rank = "A"

    def probe(self) -> dict:
        key = self.env("NASA_FIRMS_MAP_KEY")
        report = {
            "source_id": self.source_id,
            "status": "available" if key else "skip",
            "reason": "NASA_FIRMS_MAP_KEY present" if key else "NASA FIRMS area CSV API requires NASA_FIRMS_MAP_KEY.",
        }
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict) -> FeatureRows:
        key = self.env("NASA_FIRMS_MAP_KEY")
        if not key:
            raise SkipAdapter("FIRMS requires NASA_FIRMS_MAP_KEY")
        source = os.getenv("NASA_FIRMS_SOURCE", "VIIRS_SNPP_NRT")
        area = f"{region_config.get('min_lon', 122)},{region_config.get('min_lat', 20)},{region_config.get('max_lon', 154)},{region_config.get('max_lat', 46)}"
        rows: FeatureRows = []
        day = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        while day <= end:
            chunk_days = min(10, (end - day).days + 1)
            url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{key}/{source}/{area}/{chunk_days}/{day.date().isoformat()}"
            response, sample = get(url, timeout=60)
            if response is None or response.status_code != 200:
                self.failure(status="fetch_error", date=day.date().isoformat(), sample_http=sample.as_dict())
                day += timedelta(days=chunk_days)
                continue
            for row in csv.DictReader(io.StringIO(response.text)):
                date = row.get("acq_date", "")
                if not date:
                    continue
                rows.append({"date": date, "source_id": self.source_id, "feature_name": "firms_fire_count", "value": 1.0})
                try:
                    rows.append({"date": date, "source_id": self.source_id, "feature_name": "firms_brightness_mean", "value": float(row.get("brightness") or row.get("bright_ti4") or 0)})
                except Exception:
                    pass
            day += timedelta(days=chunk_days)
        if not rows:
            raise SkipAdapter("No FIRMS rows fetched")
        return rows

    def aggregate(self, rows: FeatureRows, freq: str = "1D", spatial_unit: str = "country") -> FeatureRows:
        counts: dict[str, float] = defaultdict(float)
        brightness: dict[str, list[float]] = defaultdict(list)
        for row in rows:
            if row["feature_name"] == "firms_fire_count":
                counts[str(row["date"])] += float(row["value"])
            else:
                brightness[str(row["date"])].append(float(row["value"]))
        out: FeatureRows = [{"date": d, "source_id": self.source_id, "feature_name": "firms_fire_count", "value": v} for d, v in sorted(counts.items())]
        out.extend({"date": d, "source_id": self.source_id, "feature_name": "firms_brightness_mean", "value": sum(v) / len(v)} for d, v in sorted(brightness.items()) if v)
        return out
