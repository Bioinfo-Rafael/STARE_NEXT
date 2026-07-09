from __future__ import annotations

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter


class EBirdAdapter(BaseAdapter):
    source_id = "ebird"
    display_name = "eBird"
    rank = "A"

    def probe(self) -> dict:
        token = self.env("EBIRD_API_KEY")
        report = {
            "source_id": self.source_id,
            "status": "available" if token else "skip",
            "reason": "EBIRD_API_KEY present" if token else "eBird API requires EBIRD_API_KEY; Basic Dataset also requires request/approval.",
        }
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict) -> FeatureRows:
        raise SkipAdapter("eBird fetch needs EBIRD_API_KEY plus a date-window implementation for the selected endpoint")
