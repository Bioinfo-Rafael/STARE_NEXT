from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import requests


USER_AGENT = "STARE_NEXT research probe/0.1 (contact: local research pipeline)"


@dataclass
class HttpSample:
    url: str
    final_url: str
    status_code: int | None
    content_type: str | None
    text_head: str
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


def get(url: str, *, params: dict[str, Any] | None = None, timeout: int = 30, headers: dict[str, str] | None = None) -> tuple[requests.Response | None, HttpSample]:
    try:
        merged_headers = {"User-Agent": USER_AGENT}
        if headers:
            merged_headers.update(headers)
        response = requests.get(url, params=params, timeout=timeout, headers=merged_headers)
        sample = HttpSample(
            url=url,
            final_url=response.url,
            status_code=response.status_code,
            content_type=response.headers.get("content-type"),
            text_head=response.text[:2000],
        )
        return response, sample
    except Exception as exc:
        return None, HttpSample(url=url, final_url=url, status_code=None, content_type=None, text_head="", error=repr(exc))


def json_or_none(response: requests.Response | None) -> Any | None:
    if response is None:
        return None
    try:
        return response.json()
    except json.JSONDecodeError:
        return None
