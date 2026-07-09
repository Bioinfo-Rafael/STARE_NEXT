from __future__ import annotations

from pathlib import Path
from typing import Any

from src.utils.io import append_jsonl


def log_event(output_dir: str | Path, event: str, **payload: Any) -> None:
    append_jsonl(Path(output_dir) / "run_log.jsonl", {"event": event, **payload})
