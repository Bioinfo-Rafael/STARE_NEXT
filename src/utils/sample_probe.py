from __future__ import annotations

from pathlib import Path
from typing import Mapping

from src.utils.io import write_json


def save_probe_report(output_dir: str | Path, source_id: str, report: Mapping[str, object]) -> Path:
    path = Path(output_dir) / "metadata" / "probe_reports" / f"{source_id}.json"
    write_json(path, dict(report))
    return path
