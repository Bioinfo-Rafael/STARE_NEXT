from __future__ import annotations

from src.adapters.base import StaticSkipAdapter


class MovebankAdapter(StaticSkipAdapter):
    source_id = "movebank"
    display_name = "Movebank"
    rank = "A"
    skip_reason = "Movebank generally requires account/API credentials or per-study permission; public-only unauthenticated endpoint was not configured."
