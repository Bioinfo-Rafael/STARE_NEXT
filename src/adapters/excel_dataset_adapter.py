from __future__ import annotations

import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter
from src.registry.dataset_registry import DatasetRecord
from src.utils.http import get, json_or_none


class ExcelDatasetAdapter(BaseAdapter):
    source_id = "excel_dataset"
    display_name = "Excel-listed earthquake/geodetic datasets"

    def __init__(self, records: list[DatasetRecord], *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.records = records

    def probe_dataset(self, record: DatasetRecord) -> dict[str, Any]:
        if self._is_jma_recent(record):
            response, sample = get("https://www.jma.go.jp/bosai/quake/data/list.json", timeout=20)
            data = json_or_none(response)
            report = {
                "dataset_id": record.dataset_id,
                "name": record.name,
                "status": "ok" if isinstance(data, list) else "error",
                "sample_http": sample.as_dict(),
                "sample_row": data[0] if isinstance(data, list) and data else None,
                "adapter": "jma_bosai_quake_list",
            }
        else:
            report = {
                "dataset_id": record.dataset_id,
                "name": record.name,
                "status": "skip",
                "reason": self.skip_reason(record),
                "url": record.url,
            }
        self.save_probe({"source_id": f"excel_{record.dataset_id}", **report})
        return report

    def probe(self) -> dict[str, Any]:
        sample = [self.probe_dataset(r) for r in self.records[:20]]
        report = {"source_id": self.source_id, "status": "ok", "n_records": len(self.records), "sample": sample}
        self.save_probe(report)
        return report

    def fetch_dataset(self, record: DatasetRecord, start_date: str, end_date: str, region_config: dict[str, Any]) -> FeatureRows:
        if self._is_jma_recent(record):
            return self._fetch_jma_recent(record, start_date, end_date)
        raise SkipAdapter(self.skip_reason(record))

    def _is_jma_recent(self, record: DatasetRecord) -> bool:
        blob = f"{record.provider} {record.name} {record.description} {record.url}"
        return "気象庁" in blob and ("最近の地震活動" in blob or "震源・震度" in blob or "quake/data/list" in blob or "hypo" in blob)

    def skip_reason(self, record: DatasetRecord) -> str:
        blob = f"{record.usable_status} {record.access_type} {record.notes} {record.url}"
        if "requires_registration" in blob or re.search(r"登録|ログイン|審査|申請|認証", blob):
            return "requires_registration_or_manual_terms_check"
        if not record.url:
            return "no_machine_url_in_excel"
        return "adapter_not_implemented_for_excel_dataset"

    def _fetch_jma_recent(self, record: DatasetRecord, start_date: str, end_date: str) -> FeatureRows:
        response, sample = get("https://www.jma.go.jp/bosai/quake/data/list.json", timeout=20)
        data = json_or_none(response)
        if not isinstance(data, list):
            raise SkipAdapter(f"JMA recent quake list did not return a JSON list: {sample.error or sample.status_code}")
        rows: FeatureRows = []
        for item in data:
            if not isinstance(item, dict):
                continue
            at = str(item.get("at") or item.get("rdt") or "")
            date = at[:10]
            if not (start_date <= date <= end_date):
                continue
            mag_raw = item.get("mag")
            try:
                mag = float(mag_raw)
            except Exception:
                mag = 0.0
            cod = str(item.get("cod") or "")
            lat = lon = depth_km = None
            m = re.match(r"([+-]\d+(?:\.\d+)?)([+-]\d+(?:\.\d+)?)([+-]\d+(?:\.\d+)?)/", cod)
            if m:
                lat = float(m.group(1))
                lon = float(m.group(2))
                depth_km = abs(float(m.group(3))) / 1000.0
            rows.append(
                {
                    "date": date,
                    "dataset_id": record.dataset_id,
                    "target_name": "jma_event_count",
                    "count": 1.0,
                    "m4_flag": 1.0 if mag >= 4.0 else 0.0,
                    "m5_flag": 1.0 if mag >= 5.0 else 0.0,
                    "energy": 10 ** (1.5 * mag) if mag > 0 else 0.0,
                    "magnitude": mag,
                    "lat": lat,
                    "lon": lon,
                    "depth_km": depth_km,
                    "area_name": item.get("anm", ""),
                }
            )
        aggregated = self.aggregate(rows) if rows else []
        if not aggregated:
            # The endpoint is recent-only, but still return an explicit all-zero target
            # frame for short windows that overlap no reported event.
            aggregated = []
        return self._fill_daily_targets(record.dataset_id, aggregated, start_date, end_date)

    def _fill_daily_targets(self, dataset_id: str, rows: FeatureRows, start_date: str, end_date: str) -> FeatureRows:
        targets = ["count", "m4_flag", "m5_flag", "energy", "max_magnitude"]
        indexed = {(str(r["date"]), str(r["target_name"])): float(r.get("value") or 0) for r in rows}
        out: FeatureRows = []
        day = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        while day <= end:
            ds = day.date().isoformat()
            for target in targets:
                out.append({"date": ds, "dataset_id": dataset_id, "target_name": target, "value": indexed.get((ds, target), 0.0)})
            day += timedelta(days=1)
        return out

    def aggregate(self, rows: FeatureRows, freq: str = "1D", spatial_unit: str = "country") -> FeatureRows:
        by_date: dict[str, dict[str, float]] = {}
        dataset_id = rows[0].get("dataset_id", "excel_dataset") if rows else "excel_dataset"
        for row in rows:
            bucket = by_date.setdefault(str(row["date"]), {"count": 0.0, "m4_flag": 0.0, "m5_flag": 0.0, "energy": 0.0, "max_magnitude": 0.0})
            bucket["count"] += float(row.get("count") or 0)
            bucket["m4_flag"] = max(bucket["m4_flag"], float(row.get("m4_flag") or 0))
            bucket["m5_flag"] = max(bucket["m5_flag"], float(row.get("m5_flag") or 0))
            bucket["energy"] += float(row.get("energy") or 0)
            bucket["max_magnitude"] = max(bucket["max_magnitude"], float(row.get("magnitude") or 0))
        out: FeatureRows = []
        for date, vals in sorted(by_date.items()):
            for target, value in vals.items():
                out.append({"date": date, "dataset_id": dataset_id, "target_name": target, "value": value})
        return out
