from __future__ import annotations

from datetime import datetime
from urllib.parse import quote

from src.adapters.base import BaseAdapter, FeatureRows, SkipAdapter
from src.utils.http import get, json_or_none


class WikimediaAdapter(BaseAdapter):
    source_id = "wikimedia"
    display_name = "Wikimedia Pageviews"
    rank = "S"
    articles = ["地震", "南海トラフ巨大地震", "地震雲", "宏観異常現象", "耳鳴り", "防災", "津波", "余震"]

    def _url(self, article: str, start_date: str, end_date: str) -> str:
        start = start_date.replace("-", "")
        end = end_date.replace("-", "")
        article_enc = quote(article.replace(" ", "_"), safe="")
        return (
            "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
            f"ja.wikipedia/all-access/all-agents/{article_enc}/daily/{start}/{end}"
        )

    def probe(self) -> dict:
        url = self._url("地震", "2022-01-01", "2022-01-07")
        response, sample = get(url, timeout=20)
        data = json_or_none(response)
        items = data.get("items", []) if isinstance(data, dict) else []
        report = {
            "source_id": self.source_id,
            "status": "ok" if response is not None and response.status_code == 200 and items else "error",
            "sample_http": sample.as_dict(),
            "sample_keys": list(items[0].keys()) if items else [],
            "time_grain": "daily",
            "geo_grain": "article",
            "n_sample_rows": len(items),
        }
        self.save_probe(report)
        return report

    def fetch(self, start_date: str, end_date: str, region_config: dict) -> FeatureRows:
        rows: FeatureRows = []
        for article in self.articles:
            response, sample = get(self._url(article, start_date, end_date), timeout=30)
            data = json_or_none(response)
            if response is None or response.status_code != 200 or not isinstance(data, dict):
                self.failure(status="fetch_error", article=article, sample_http=sample.as_dict())
                continue
            for item in data.get("items", []):
                ts = str(item.get("timestamp", ""))
                date = f"{ts[:4]}-{ts[4:6]}-{ts[6:8]}" if len(ts) >= 8 else ""
                rows.append(
                    {
                        "date": date,
                        "source_id": self.source_id,
                        "feature_name": f"pageviews_{article}",
                        "value": float(item.get("views") or 0),
                        "article": article,
                    }
                )
        if not rows:
            raise SkipAdapter("No Wikimedia rows fetched; see failures.jsonl")
        return rows

    def aggregate(self, rows: FeatureRows, freq: str = "1D", spatial_unit: str = "country") -> FeatureRows:
        by_key: dict[tuple[str, str], float] = {}
        total: dict[str, float] = {}
        for row in rows:
            date = row["date"]
            feature = row["feature_name"]
            by_key[(date, feature)] = by_key.get((date, feature), 0.0) + float(row["value"])
            total[date] = total.get(date, 0.0) + float(row["value"])
        out = [{"date": d, "feature_name": f, "value": v, "source_id": self.source_id} for (d, f), v in sorted(by_key.items())]
        out.extend({"date": d, "feature_name": "pageviews_total", "value": v, "source_id": self.source_id} for d, v in sorted(total.items()))
        return out
