from __future__ import annotations

from collections import defaultdict

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter
from src.utils.http import get, json_or_none


class OpenAqAdapter(BaseAdapter):
    source_id = "openaq"
    display_name = "OpenAQ"
    rank = "A"
    url = "https://api.openaq.org/v3/measurements"

    def probe(self) -> dict:
        key = self.env("OPENAQ_API_KEY")
        if not key:
            report = {"source_id": self.source_id, "status": "skip", "reason": "OpenAQ v3 requires OPENAQ_API_KEY in .env or environment."}
            self.save_probe(report)
            return report
        response, sample = get(
            self.url,
            params={"coordinates": "35.681,139.767", "radius": 50000, "limit": 1},
            headers={"X-API-Key": key},
            timeout=20,
        )
        data = json_or_none(response)
        status = "ok" if isinstance(data, dict) and response is not None and response.status_code == 200 else "skip"
        report = {
            "source_id": self.source_id,
            "status": status,
            "sample_http": sample.as_dict(),
            "sample_keys": list(data.keys()) if isinstance(data, dict) else [],
            "reason": "OpenAQ v3 queried with OPENAQ_API_KEY.",
        }
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict) -> FeatureRows:
        key = self.env("OPENAQ_API_KEY")
        if not key:
            raise SkipAdapter("OpenAQ requires OPENAQ_API_KEY")
        response, sample = get(
            self.url,
            params={
                "coordinates": "35.681,139.767",
                "radius": 100000,
                "date_from": f"{start_date}T00:00:00Z",
                "date_to": f"{end_date}T23:59:59Z",
                "limit": 1000,
            },
            headers={"X-API-Key": key},
            timeout=60,
        )
        data = json_or_none(response)
        if not isinstance(data, dict) or not isinstance(data.get("results"), list):
            raise SkipAdapter(f"OpenAQ did not return measurements list: {sample.error or sample.status_code}")
        rows: FeatureRows = []
        for item in data["results"]:
            dt = ((item.get("period") or {}).get("datetimeFrom") or {}).get("utc") or ((item.get("date") or {}).get("utc") or "")
            date = str(dt)[:10]
            parameter = item.get("parameter") or item.get("parameterId") or "unknown"
            try:
                value = float(item.get("value"))
            except Exception:
                continue
            if date:
                rows.append({"date": date, "source_id": self.source_id, "feature_name": f"openaq_{parameter}", "value": value})
        if not rows:
            raise SkipAdapter("No OpenAQ measurements found in requested range")
        return self.aggregate(rows)

    def aggregate(self, rows: FeatureRows, freq: str = "1D", spatial_unit: str = "country") -> FeatureRows:
        vals: dict[tuple[str, str], list[float]] = defaultdict(list)
        for row in rows:
            vals[(str(row["date"]), str(row["feature_name"]))].append(float(row["value"]))
        return [{"date": d, "source_id": self.source_id, "feature_name": f, "value": sum(v) / len(v)} for (d, f), v in sorted(vals.items())]
