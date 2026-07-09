from __future__ import annotations

import traceback
from typing import Callable, TypeVar

from src.utils.io import append_jsonl

T = TypeVar("T")


def safe_call(label: str, failures_path: str, fn: Callable[[], T]) -> T | None:
    try:
        return fn()
    except Exception as exc:
        append_jsonl(
            failures_path,
            {
                "label": label,
                "status": "error",
                "error_type": type(exc).__name__,
                "error_message": str(exc),
                "traceback": traceback.format_exc(limit=8),
            },
        )
        return None
