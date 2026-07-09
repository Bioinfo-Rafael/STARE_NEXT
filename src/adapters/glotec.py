from __future__ import annotations

from src.adapters.base import StaticSkipAdapter


class GlotecAdapter(StaticSkipAdapter):
    source_id = "glotec"
    display_name = "NOAA GloTEC / TEC anomaly"
    rank = "S"
    skip_reason = (
        "GloTEC products are typically NetCDF/space-weather grids; add a stable product URL and netCDF parser before automated fetch. "
        "Probe report records this as a planned adapter instead of guessing a raw endpoint."
    )
