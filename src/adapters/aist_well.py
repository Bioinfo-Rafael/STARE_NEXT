from __future__ import annotations

from src.adapters.base import StaticSkipAdapter


class AistWellAdapter(StaticSkipAdapter):
    source_id = "aist_well"
    display_name = "AIST Well Web / groundwater strain temperature"
    rank = "S"
    skip_reason = "AIST groundwater/well data requires source-specific access checks; do not scrape until terms and download endpoints are confirmed."
