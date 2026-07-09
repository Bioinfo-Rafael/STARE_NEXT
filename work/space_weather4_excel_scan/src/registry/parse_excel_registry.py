from __future__ import annotations

import csv
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from src.registry.classify_excel_datasets import infer_geo_type, infer_temporal_type, usable_status
from src.registry.dataset_registry import DatasetRecord
from src.utils.io import ensure_dir, write_csv, write_json

NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def _colnum(ref: str) -> int:
    m = re.match(r"([A-Z]+)", ref)
    n = 0
    for ch in (m.group(1) if m else "A"):
        n = n * 26 + ord(ch) - 64
    return n - 1


def _clean(text: object) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def _slug(text: str, fallback: str) -> str:
    text = re.sub(r"https?://", "", text)
    text = re.sub(r"[^0-9A-Za-zぁ-んァ-ヶ一-龠ー]+", "_", text).strip("_")
    return text[:90] or fallback


def read_xlsx_rows(path: str | Path) -> dict[str, list[list[str]]]:
    with zipfile.ZipFile(path) as z:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("a:si", NS):
                shared.append("".join(t.text or "" for t in si.iter(f"{{{NS['a']}}}t")))
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        rid_to_target = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
        out: dict[str, list[list[str]]] = {}
        for sh in wb.find("a:sheets", NS) or []:
            name = sh.attrib["name"]
            target = rid_to_target[sh.attrib[f"{{{NS['r']}}}id"]]
            sheet_path = "xl/" + target if not target.startswith("/") else target[1:]
            root = ET.fromstring(z.read(sheet_path))
            rows: list[list[str]] = []
            for row in root.findall(".//a:sheetData/a:row", NS):
                cells: list[tuple[int, str]] = []
                maxc = -1
                for c in row.findall("a:c", NS):
                    idx = _colnum(c.attrib.get("r", "A1"))
                    value = ""
                    if c.attrib.get("t") == "inlineStr":
                        value = "".join(t.text or "" for t in c.iter(f"{{{NS['a']}}}t"))
                    else:
                        v = c.find("a:v", NS)
                        if v is not None:
                            raw = v.text or ""
                            value = shared[int(raw)] if c.attrib.get("t") == "s" and raw.isdigit() else raw
                    cells.append((idx, _clean(value)))
                    maxc = max(maxc, idx)
                vals = [""] * (maxc + 1)
                for idx, value in cells:
                    vals[idx] = value
                rows.append(vals)
            out[name] = rows
        return out


def _find_header_row(rows: list[list[str]]) -> int:
    best = 0
    score = -1
    for i, row in enumerate(rows[:20]):
        joined = " ".join(row)
        s = sum(k in joined for k in ["分類", "所管", "データ名", "概要", "URL", "データ種別"]) + sum(bool(v) for v in row)
        if s > score and ("URL" in joined or "データ名" in joined):
            best = i
            score = s
    return best


def _headers(rows: list[list[str]], idx: int) -> list[str]:
    top = rows[idx] if idx < len(rows) else []
    sub = rows[idx + 1] if idx + 1 < len(rows) else []
    width = max(len(top), len(sub))
    out: list[str] = []
    last = ""
    for i in range(width):
        h = _clean(top[i] if i < len(top) else "")
        s = _clean(sub[i] if i < len(sub) else "")
        if h:
            last = h
        name = h or last or f"col_{i+1}"
        if s and s not in name:
            name = f"{name}_{s}"
        out.append(name)
    return out


def _pick(row: dict[str, str], pats: list[str]) -> str:
    for pat in pats:
        rx = re.compile(pat)
        for key, value in row.items():
            if rx.search(key) and value:
                return value
    return ""


def parse_excel_registry(excel_path: str | Path, output_dir: str | Path) -> list[DatasetRecord]:
    rows_by_sheet = read_xlsx_rows(excel_path)
    inspection: dict[str, Any] = {"workbook": str(excel_path), "sheets": []}
    records: list[DatasetRecord] = []
    for sheet, rows in rows_by_sheet.items():
        max_cols = max((len(r) for r in rows[:12]), default=0)
        inspection["sheets"].append({"sheet_name": sheet, "first_10_rows": [r[:max_cols] for r in rows[:10]]})
        if not rows:
            continue
        header_idx = _find_header_row(rows)
        headers = _headers(rows, header_idx)
        start = header_idx + 2
        for rnum, vals in enumerate(rows[start:], start=start + 1):
            if not any(vals):
                continue
            row = {headers[i] if i < len(headers) else f"col_{i+1}": vals[i] for i in range(len(vals))}
            name = _pick(row, [r"データ名", r"データベース", r"サイト", r"情報"])
            url = _pick(row, [r"URL"])
            provider = _pick(row, [r"所管", r"提供", r"機関"])
            category = _pick(row, [r"分類"])
            description = _pick(row, [r"概要", r"説明"])
            data_type = _pick(row, [r"データ種別"])
            data_items = _pick(row, [r"データ項目"])
            public_status = _pick(row, [r"公開状況"])
            fmt = _pick(row, [r"形式", r"拡張子"])
            access_notes = _pick(row, [r"取得", r"備考"])
            if not name and not url:
                continue
            blob = " ".join([category, provider, name, description, data_type, data_items, public_status, fmt, access_notes, url])
            temporal = infer_temporal_type(blob)
            geo = infer_geo_type(blob)
            rec = DatasetRecord(
                excel_dataset_id=_slug(f"{provider}_{name}", f"{sheet}_{rnum}"),
                category=category,
                provider=provider,
                name=name,
                description=description,
                url=url,
                data_type=data_type,
                data_items=data_items,
                public_status=public_status,
                format=fmt,
                access_notes=access_notes,
                inferred_temporal_type=temporal,
                inferred_geo_type=geo,
                usable_status=usable_status(blob, url, temporal),
                sheet_name=sheet,
                source_row=rnum,
            )
            records.append(rec)
    meta = ensure_dir(Path(output_dir) / "metadata")
    write_json(meta / "excel_inspection.json", inspection)
    fields = list(DatasetRecord("").as_dict().keys())
    write_csv(meta / "dataset_registry.csv", [r.as_dict() for r in records], fields)
    return records


def load_registry_csv(path: str | Path) -> list[DatasetRecord]:
    with Path(path).open(newline="", encoding="utf-8") as f:
        return [DatasetRecord(**row) for row in csv.DictReader(f)]
