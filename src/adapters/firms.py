from __future__ import annotations

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter


class FirmsAdapter(BaseAdapter):
    source_id = "firms"
    display_name = "NASA FIRMS"
    rank = "A"

    def probe(self) -> dict:
        key = self.env("NASA_FIRMS_MAP_KEY")
        report = {
            "source_id": self.source_id,
            "status": "available" if key else "skip",
            "reason": "NASA_FIRMS_MAP_KEY present" if key else "NASA FIRMS area CSV API requires NASA_FIRMS_MAP_KEY.",
        }
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict) -> FeatureRows:
        raise SkipAdapter("FIRMS fetch requires NASA_FIRMS_MAP_KEY and API-specific date chunking")
