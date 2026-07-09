from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class DatasetRecord:
    excel_dataset_id: str
    category: str = ""
    provider: str = ""
    name: str = ""
    description: str = ""
    url: str = ""
    data_type: str = ""
    data_items: str = ""
    public_status: str = ""
    format: str = ""
    access_notes: str = ""
    inferred_temporal_type: str = "unknown"
    inferred_geo_type: str = "unknown"
    usable_status: str = "unknown"
    sheet_name: str = ""
    source_row: int = 0

    def as_dict(self) -> dict[str, object]:
        return asdict(self)
