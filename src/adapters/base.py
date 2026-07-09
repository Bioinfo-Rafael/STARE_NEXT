from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

from src.utils.io import append_jsonl, ensure_dir
from src.utils.sample_probe import save_probe_report

FeatureRows = list[dict[str, Any]]


class AdapterError(RuntimeError):
    pass


class SkipAdapter(AdapterError):
    pass


class BaseAdapter:
    source_id = "base"
    display_name = "Base Adapter"
    rank = ""

    def __init__(self, output_dir: str | Path = "results", raw_dir: str | Path = "cache/raw", keep_raw: bool = False):
        self.output_dir = Path(output_dir)
        self.raw_dir = Path(raw_dir) / self.source_id
        self.keep_raw = keep_raw
        ensure_dir(self.output_dir / "metadata" / "probe_reports")
        ensure_dir(self.raw_dir)

    def probe(self) -> dict[str, Any]:
        report = {"source_id": self.source_id, "status": "skip", "reason": "probe not implemented"}
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict[str, Any]) -> FeatureRows:
        raise SkipAdapter("fetch not implemented")

    def normalize(self, raw: Any) -> FeatureRows:
        return raw if isinstance(raw, list) else []

    def aggregate(self, rows: FeatureRows, freq: str = "1D", spatial_unit: str = "country") -> FeatureRows:
        return rows

    def cleanup(self) -> None:
        if not self.keep_raw and self.raw_dir.exists():
            shutil.rmtree(self.raw_dir, ignore_errors=True)

    def save_probe(self, report: dict[str, Any]) -> None:
        save_probe_report(self.output_dir, self.source_id, report)

    def failure(self, **payload: Any) -> None:
        payload.setdefault("source_id", self.source_id)
        append_jsonl(self.output_dir / "failures.jsonl", payload)

    def env(self, name: str) -> str | None:
        return os.getenv(name)


class StaticSkipAdapter(BaseAdapter):
    skip_reason = "not configured"

    def probe(self) -> dict[str, Any]:
        report = {
            "source_id": self.source_id,
            "display_name": self.display_name,
            "status": "skip",
            "reason": self.skip_reason,
        }
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict[str, Any]) -> FeatureRows:
        raise SkipAdapter(self.skip_reason)
