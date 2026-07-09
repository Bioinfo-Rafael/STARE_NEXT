from __future__ import annotations

from src.adapters import EXTERNAL_ADAPTERS


def create_external_adapter(source_id: str, **kwargs):
    if source_id not in EXTERNAL_ADAPTERS:
        raise KeyError(f"Unknown external adapter: {source_id}")
    return EXTERNAL_ADAPTERS[source_id](**kwargs)
