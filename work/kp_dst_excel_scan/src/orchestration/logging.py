from __future__ import annotations

from pathlib import Path

from src.utils.io import append_jsonl


def log_event(output_dir: str | Path, event: str, **payload) -> None:
    append_jsonl(Path(output_dir) / "metadata" / "run_log.jsonl", {"event": event, **payload})
