from __future__ import annotations

from collections import defaultdict

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter
from src.utils.http import get, json_or_none


class KpDstAdapter(BaseAdapter):
    source_id = "kp_dst"
    display_name = "NOAA Kp index / Dst companion"
    rank = "S"
    kp_url = "https://kp.gfz.de/app/json/"

    def probe(self) -> dict:
        response, sample = get(
            self.kp_url,
            params={"start": "2020-01-01T00:00:00Z", "end": "2020-01-03T23:59:59Z", "index": "Kp", "status": "def"},
            timeout=20,
        )
        data = json_or_none(response)
        report = {
            "source_id": self.source_id,
            "status": "ok" if isinstance(data, dict) and data.get("Kp") else "error",
            "sample_http": sample.as_dict(),
            "sample_keys": list(data.keys()) if isinstance(data, dict) else [],
            "sample_row": {"datetime": data.get("datetime", [None])[0], "Kp": data.get("Kp", [None])[0]} if isinstance(data, dict) and data.get("Kp") else None,
            "note": "Kp uses GFZ official JSON API for historical data. Dst remains a planned Kyoto WDC extension.",
        }
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict) -> FeatureRows:
        response, sample = get(
            self.kp_url,
            params={"start": f"{start_date}T00:00:00Z", "end": f"{end_date}T23:59:59Z", "index": "Kp", "status": "all"},
            timeout=60,
        )
        data = json_or_none(response)
        if not isinstance(data, dict) or not data.get("Kp") or not data.get("datetime"):
            raise SkipAdapter(f"GFZ Kp endpoint did not return Kp JSON arrays: {sample.error or sample.status_code}")
        rows: FeatureRows = []
        for dt, kp in zip(data["datetime"], data["Kp"]):
            date = str(dt)[:10]
            if start_date <= date <= end_date:
                rows.append({"date": date, "source_id": self.source_id, "feature_name": "kp_index", "value": float(kp or 0)})
        if not rows:
            raise SkipAdapter("GFZ Kp endpoint returned no rows in requested date range")
        return rows

    def aggregate(self, rows: FeatureRows, freq: str = "1D", spatial_unit: str = "country") -> FeatureRows:
        vals: dict[tuple[str, str], list[float]] = defaultdict(list)
        for row in rows:
            vals[(row["date"], "kp_mean")].append(float(row["value"]))
            vals[(row["date"], "kp_max")].append(float(row["value"]))
        out: FeatureRows = []
        for (date, feature), values in sorted(vals.items()):
            value = max(values) if feature.endswith("_max") else sum(values) / len(values)
            out.append({"date": date, "source_id": self.source_id, "feature_name": feature, "value": value})
        return out
