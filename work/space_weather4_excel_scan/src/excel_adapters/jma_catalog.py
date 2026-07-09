from __future__ import annotations

import re
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from src.excel_adapters.base import BaseExcelAdapter
from src.registry.dataset_registry import DatasetRecord
from src.utils.dates import date_range
from src.utils.http import get
from src.utils.io import ensure_dir, write_json


class JmaCatalogAdapter(BaseExcelAdapter):
    adapter_name = "jma_catalog"

    def can_handle(self, record: DatasetRecord) -> bool:
        blob = f"{record.provider} {record.name} {record.description} {record.url}"
        return "気象庁" in blob and ("地震月報" in blob or "カタログ" in blob or "bulletin" in blob)

    def probe(self, record: DatasetRecord) -> dict[str, Any]:
        response, sample = get("https://www.data.jma.go.jp/eqev/data/bulletin/hypo_e.html", timeout=20)
        years = sorted({int(y) for y in re.findall(r'href="\./data/hypo/h(20\d\d)\.zip"', response.text if response else "")})
        report = self._report(
            record,
            "ok" if years else "skip",
            sample_http=sample.as_dict(),
            guessed_format="yearly_zip_fixed_width",
            requires_login_or_manual_download=False,
            parser_status="implemented" if years else "no_year_links",
            reason="" if years else "no_year_links_found",
        )
        report["available_years"] = years
        write_json(self.output_dir / "metadata" / "probe_reports" / f"{record.excel_dataset_id}.json", report)
        return report

    def _available_years(self) -> set[int]:
        response, _sample = get("https://www.data.jma.go.jp/eqev/data/bulletin/hypo_e.html", timeout=20)
        if response is None or response.status_code != 200:
            return set()
        return {int(y) for y in re.findall(r'href="\./data/hypo/h(20\d\d)\.zip"', response.text)}

    def _parse_float(self, text: str, scale: float) -> float | None:
        text = text.strip()
        if not text:
            return None
        try:
            return float(text) / scale
        except Exception:
            return None

    def _parse_mag(self, text: str) -> float:
        text = text.strip()
        if not text:
            return 0.0
        if len(text) == 2 and text[0].isalpha():
            return -(ord(text[0].upper()) - ord("A") + 1) - int(text[1]) / 10
        try:
            return float(text) / 10
        except Exception:
            return 0.0

    def _parse_line(self, line: str, dataset_id: str) -> dict | None:
        if len(line) < 54 or line[0] not in {"J", "U", "I"}:
            return None
        try:
            year, month, day = int(line[1:5]), int(line[5:7]), int(line[7:9])
            hour, minute = int(line[9:11]), int(line[11:13])
            sec = int(line[13:17].strip() or "0") / 100
            dt = datetime(year, month, day, hour, minute, min(int(sec), 59))
        except Exception:
            return None
        lat_deg = self._parse_float(line[21:24], 1)
        lat_min = self._parse_float(line[24:28], 100)
        lon_deg = self._parse_float(line[32:36], 1)
        lon_min = self._parse_float(line[36:40], 100)
        depth = self._parse_float(line[44:49], 100)
        mag = self._parse_mag(line[52:54])
        lat = lat_deg + lat_min / 60 if lat_deg is not None and lat_min is not None else None
        lon = lon_deg + lon_min / 60 if lon_deg is not None and lon_min is not None else None
        return {"datetime": dt.isoformat(), "date": dt.date().isoformat(), "magnitude": mag, "depth_km": depth, "lat": lat, "lon": lon, "dataset_id": dataset_id}

    def fetch(self, record: DatasetRecord, start_date: str, end_date: str) -> list[dict]:
        available = self._available_years()
        rows: list[dict] = []
        cache = ensure_dir(self.raw_dir / "jma_catalog")
        for year in range(int(start_date[:4]), int(end_date[:4]) + 1):
            if available and year not in available:
                self.failure({"excel_dataset_id": record.excel_dataset_id, "status": "year_unavailable", "year": year, "reason": "not linked from hypo_e.html"})
                continue
            path = cache / f"h{year}.zip"
            if not path.exists():
                url = f"https://www.data.jma.go.jp/eqev/data/bulletin/data/hypo/h{year}.zip"
                response, sample = get(url, timeout=60)
                if response is None or response.status_code != 200:
                    self.failure({"excel_dataset_id": record.excel_dataset_id, "status": "fetch_error", "year": year, "sample_http": sample.as_dict()})
                    continue
                path.write_bytes(response.content)
            with zipfile.ZipFile(path) as zf:
                for name in zf.namelist():
                    text = zf.read(name).decode("shift_jis", errors="replace")
                    for line in text.splitlines():
                        parsed = self._parse_line(line, record.excel_dataset_id)
                        if parsed and start_date <= parsed["date"] <= end_date:
                            rows.append(parsed)
        return rows

    def aggregate(self, record: DatasetRecord, rows: list[dict], start_date: str, end_date: str, spatial_unit: str) -> list[dict]:
        by_date: dict[str, list[dict]] = {d: [] for d in date_range(start_date, end_date)}
        for row in rows:
            by_date.setdefault(row["date"], []).append(row)
        out: list[dict] = []
        for date, events in sorted(by_date.items()):
            mags = [float(e["magnitude"]) for e in events]
            depths = [float(e["depth_km"] or 0) for e in events]
            targets = {
                "count": len(events),
                "m3_flag": 1 if any(m >= 3 for m in mags) else 0,
                "m4_flag": 1 if any(m >= 4 for m in mags) else 0,
                "m5_flag": 1 if any(m >= 5 for m in mags) else 0,
                "m6_flag": 1 if any(m >= 6 for m in mags) else 0,
                "max_magnitude": max(mags) if mags else 0.0,
                "energy": sum(10 ** (1.5 * m) for m in mags if m > 0),
                "mean_depth": sum(depths) / len(depths) if depths else 0.0,
                "shallow_count": sum(1 for d in depths if d <= 30),
                "deep_count": sum(1 for d in depths if d >= 100),
                "intensity_ge_3_count": "",
                "intensity_ge_4_count": "",
                "intensity_ge_5_count": "",
            }
            for target, value in targets.items():
                if value == "":
                    continue
                out.append({"date": date, "target_name": target, "target_type": "event_catalog", "spatial_unit": spatial_unit, "region": "national", "value": float(value)})
        return out
