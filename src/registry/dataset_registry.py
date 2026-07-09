from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class DatasetRecord:
    dataset_id: str
    name: str
    category: str = ""
    provider: str = ""
    description: str = ""
    url: str = ""
    access_type: str = ""
    notes: str = ""
    usable_status: str = "unknown"
    sheet_name: str = ""
    source_row: int = 0

    def as_dict(self) -> dict[str, object]:
        return asdict(self)
