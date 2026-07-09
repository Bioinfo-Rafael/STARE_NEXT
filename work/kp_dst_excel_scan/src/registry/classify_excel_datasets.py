from __future__ import annotations

import re


def infer_temporal_type(text: str) -> str:
    if re.search(r"波形|強震|K-NET|KiK-net|DONET|F-net.*波形", text, re.I):
        return "waveform"
    if re.search(r"活断層|地質|地下構造|地形|ハザード|J-SHIS|地震動予測|地図|地盤", text, re.I):
        return "static_spatial"
    if re.search(r"GNSS|GEONET|潮位|NOWPHAS|地下水|水温|歪|ひずみ|地磁気|験潮|連続観測", text, re.I):
        return "time_series"
    if re.search(r"震源|震度|地震月報|カタログ|最近の地震活動|メカニズム|発震機構|F-net|Hi-net", text, re.I):
        return "event_catalog"
    if re.search(r"観測点|一覧|文献|会報|基礎知識", text, re.I):
        return "static_metadata"
    return "unknown"


def infer_geo_type(text: str) -> str:
    if re.search(r"観測点|GNSS|GEONET|験潮|地下水|地磁気|station", text, re.I):
        return "station"
    if re.search(r"緯度|経度|震源|震央|位置|point", text, re.I):
        return "point"
    if re.search(r"メッシュ|mesh|地図|ハザード|地盤", text, re.I):
        return "mesh"
    if re.search(r"活断層|ポリゴン|polygon|区域|地域", text, re.I):
        return "polygon"
    if re.search(r"全国|日本|national", text, re.I):
        return "national"
    return "unknown"


def usable_status(text: str, url: str, temporal_type: str) -> str:
    if re.search(r"ログイン|登録|申請|審査|認証|アカウント", text, re.I):
        return "requires_login"
    if not url:
        return "skip"
    if temporal_type == "static_spatial":
        return "static_only"
    if re.search(r"PDF|手動|ダウンロード|利用規約", text, re.I):
        return "requires_manual_download"
    if temporal_type in {"event_catalog", "time_series"}:
        return "usable"
    if temporal_type == "waveform":
        return "probe_only"
    return "probe_only"
