from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover - fallback for bare Python environments
    requests = None
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

USER_AGENT = "STARE_NEXT kp-dst focused scan/0.1"


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


def get(url: str, *, params: dict[str, Any] | None = None, timeout: int = 30) -> tuple[requests.Response | None, HttpSample]:
    if requests is None:
        final_url = url + (("?" + urlencode(params)) if params else "")
        try:
            req = Request(final_url, headers={"User-Agent": USER_AGENT})
            with urlopen(req, timeout=timeout) as response:
                data = response.read()
                text = data.decode("utf-8", errors="replace")
                wrapper = _UrllibResponse(final_url, response.status, response.headers.get("content-type"), text, data)
                return wrapper, HttpSample(url=url, final_url=final_url, status_code=response.status, content_type=response.headers.get("content-type"), text_head=text[:2000])
        except Exception as exc:
            return None, HttpSample(url=url, final_url=final_url, status_code=None, content_type=None, text_head="", error=repr(exc))
    try:
        response = requests.get(url, params=params, timeout=timeout, headers={"User-Agent": USER_AGENT})
        return response, HttpSample(
            url=url,
            final_url=response.url,
            status_code=response.status_code,
            content_type=response.headers.get("content-type"),
            text_head=response.text[:2000],
        )
    except Exception as exc:
        return None, HttpSample(url=url, final_url=url, status_code=None, content_type=None, text_head="", error=repr(exc))


def json_or_none(response: requests.Response | None):
    if response is None:
        return None
    try:
        return response.json()
    except Exception:
        return None


class _UrllibResponse:
    def __init__(self, url: str, status_code: int, content_type: str | None, text: str, content: bytes):
        self.url = url
        self.status_code = status_code
        self.headers = {"content-type": content_type or ""}
        self.text = text
        self.content = content

    def json(self):
        return json.loads(self.text)
