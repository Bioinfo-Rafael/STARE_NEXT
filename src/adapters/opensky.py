from __future__ import annotations

from datetime import datetime, timezone

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter
from src.utils.http import get, json_or_none


class OpenSkyAdapter(BaseAdapter):
    source_id = "opensky"
    display_name = "OpenSky Network"
    rank = "A"
    url = "https://opensky-network.org/api/states/all"

    def _params(self, region_config: dict | None = None) -> dict:
        region_config = region_config or {}
        return {
            "lamin": region_config.get("min_lat", 20),
            "lomin": region_config.get("min_lon", 122),
            "lamax": region_config.get("max_lat", 46),
            "lomax": region_config.get("max_lon", 154),
        }

    def probe(self) -> dict:
        response, sample = get(self.url, params=self._params(), timeout=20)
        data = json_or_none(response)
        states = data.get("states") if isinstance(data, dict) else None
        report = {
            "source_id": self.source_id,
            "status": "ok" if isinstance(states, list) else "error",
            "sample_http": sample.as_dict(),
            "state_count": len(states) if isinstance(states, list) else None,
            "note": "Unauthenticated endpoint provides current state vectors only; historical aggregation needs credentials or archive access.",
        }
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict) -> FeatureRows:
        response, sample = get(self.url, params=self._params(region_config), timeout=20)
        data = json_or_none(response)
        if not isinstance(data, dict) or not isinstance(data.get("states"), list):
            raise SkipAdapter(f"OpenSky returned unexpected response: {sample.error or sample.status_code}")
        date = datetime.fromtimestamp(float(data.get("time")), tz=timezone.utc).date().isoformat()
        if not (start_date <= date <= end_date):
            raise SkipAdapter("OpenSky unauthenticated endpoint is current-only and outside requested range")
        states = data["states"]
        return [
            {"date": date, "source_id": self.source_id, "feature_name": "opensky_aircraft_count", "value": float(len(states))},
            {
                "date": date,
                "source_id": self.source_id,
                "feature_name": "opensky_mean_velocity",
                "value": sum(float(s[9] or 0) for s in states) / max(len(states), 1),
            },
        ]
