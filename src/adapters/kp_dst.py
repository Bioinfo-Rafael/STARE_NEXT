from __future__ import annotations

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter
from src.utils.http import get, json_or_none


class KpDstAdapter(BaseAdapter):
    source_id = "kp_dst"
    display_name = "NOAA Kp index / Dst companion"
    rank = "S"
    kp_url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"

    def probe(self) -> dict:
        response, sample = get(self.kp_url, timeout=20)
        data = json_or_none(response)
        report = {
            "source_id": self.source_id,
            "status": "ok" if isinstance(data, list) and data else "error",
            "sample_http": sample.as_dict(),
            "sample_row": data[0] if isinstance(data, list) and data else None,
            "note": "NOAA Kp endpoint covers recent values. Dst is not fetched unless a stable machine endpoint is added.",
        }
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict) -> FeatureRows:
        response, sample = get(self.kp_url, timeout=20)
        data = json_or_none(response)
        if not isinstance(data, list):
            raise SkipAdapter(f"Kp endpoint did not return JSON list: {sample.error or sample.status_code}")
        rows: FeatureRows = []
        for item in data:
            if not isinstance(item, dict):
                continue
            date = str(item.get("time_tag", ""))[:10]
            if start_date <= date <= end_date:
                rows.append({"date": date, "source_id": self.source_id, "feature_name": "kp_index", "value": float(item.get("Kp") or 0)})
                rows.append({"date": date, "source_id": self.source_id, "feature_name": "kp_station_count", "value": float(item.get("station_count") or 0)})
        if not rows:
            raise SkipAdapter("NOAA Kp endpoint is recent-only and has no rows in requested date range")
        return self.aggregate(rows)

    def aggregate(self, rows: FeatureRows, freq: str = "1D", spatial_unit: str = "country") -> FeatureRows:
        vals: dict[tuple[str, str], list[float]] = {}
        for row in rows:
            vals.setdefault((row["date"], row["feature_name"]), []).append(float(row["value"]))
        return [
            {"date": d, "source_id": self.source_id, "feature_name": f, "value": sum(v) / len(v)}
            for (d, f), v in sorted(vals.items())
        ]
