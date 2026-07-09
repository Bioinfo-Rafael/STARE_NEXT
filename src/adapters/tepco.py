from __future__ import annotations

import csv
import io
from collections import defaultdict
from datetime import datetime

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter
from src.utils.http import get


class TepcoAdapter(BaseAdapter):
    source_id = "tepco"
    display_name = "TEPCO power demand"
    rank = "A"
    candidate_url = "https://www.tepco.co.jp/forecast/html/images/juyo-d1-j.csv"

    def probe(self) -> dict:
        response, sample = get(self.candidate_url, timeout=20)
        ok = response is not None and response.status_code == 200 and "csv" in (sample.content_type or sample.text_head[:100].lower())
        report = {
            "source_id": self.source_id,
            "status": "ok" if ok else "skip",
            "candidate_url": self.candidate_url,
            "sample_http": sample.as_dict(),
            "reason": "Candidate CSV endpoint checked; historical archive support is not assumed.",
        }
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict) -> FeatureRows:
        start_year = datetime.fromisoformat(start_date).year
        end_year = datetime.fromisoformat(end_date).year
        hourly: FeatureRows = []
        for year in range(start_year, end_year + 1):
            url = f"https://www.tepco.co.jp/forecast/html/images/juyo-{year}.csv"
            response, sample = get(url, timeout=30)
            if response is None or response.status_code != 200:
                self.failure(status="fetch_error", year=year, sample_http=sample.as_dict())
                continue
            lines = [line for line in response.content.decode("cp932", errors="replace").splitlines() if line.strip()]
            header_idx = next((i for i, line in enumerate(lines) if line.startswith("DATE,")), None)
            if header_idx is None:
                self.failure(status="unexpected_schema", year=year, sample_http=sample.as_dict(), sample_lines=lines[:5])
                continue
            for row in csv.DictReader(io.StringIO("\n".join(lines[header_idx:]))):
                if not row.get("DATE") or not row.get("TIME"):
                    continue
                date = row["DATE"].replace("/", "-")
                try:
                    date = datetime.strptime(row["DATE"], "%Y/%m/%d").date().isoformat()
                except Exception:
                    pass
                if not (start_date <= date <= end_date):
                    continue
                value = next((v for k, v in row.items() if k not in {"DATE", "TIME"} and str(v).strip()), "")
                try:
                    hourly.append({"date": date, "source_id": self.source_id, "feature_name": "tepco_demand_10mw", "value": float(value)})
                except Exception:
                    continue
        if not hourly:
            raise SkipAdapter("No TEPCO annual CSV rows fetched in requested date range")
        return hourly

    def aggregate(self, rows: FeatureRows, freq: str = "1D", spatial_unit: str = "country") -> FeatureRows:
        vals: dict[str, list[float]] = defaultdict(list)
        for row in rows:
            vals[str(row["date"])].append(float(row["value"]))
        out: FeatureRows = []
        for date, values in sorted(vals.items()):
            out.append({"date": date, "source_id": self.source_id, "feature_name": "tepco_demand_mean_10mw", "value": sum(values) / len(values)})
            out.append({"date": date, "source_id": self.source_id, "feature_name": "tepco_demand_max_10mw", "value": max(values)})
        return out
