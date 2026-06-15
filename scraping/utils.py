"""Shared helpers for the source scrapers."""
from __future__ import annotations

import html
import re
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

DEFAULT_HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

REDDIT_HEADERS = {
    "User-Agent": "off-campus-housing-rag-usm/0.1 (educational project)",
    "Accept": "application/json",
}


class FetchError(RuntimeError):
    pass


def fetch_html(url: str, *, headers: Optional[dict] = None, timeout: int = 20) -> str:
    """GET a URL and return the raw HTML body. Raises FetchError on non-200."""
    h = dict(DEFAULT_HEADERS)
    if headers:
        h.update(headers)
    try:
        resp = requests.get(url, headers=h, timeout=timeout)
    except requests.RequestException as e:
        raise FetchError(f"network error: {e}") from e
    if resp.status_code != 200:
        raise FetchError(f"HTTP {resp.status_code} for {url}")
    return resp.text


def fetch_json(url: str, *, headers: Optional[dict] = None, timeout: int = 20):
    h = dict(REDDIT_HEADERS)
    if headers:
        h.update(headers)
    try:
        resp = requests.get(url, headers=h, timeout=timeout)
    except requests.RequestException as e:
        raise FetchError(f"network error: {e}") from e
    if resp.status_code != 200:
        raise FetchError(f"HTTP {resp.status_code} for {url}")
    try:
        return resp.json()
    except ValueError as e:
        raise FetchError(f"invalid JSON from {url}: {e}") from e


_WS = re.compile(r"[ \t ]+")
_MULTI_NL = re.compile(r"\n{3,}")


def clean_text(text: str) -> str:
    """Normalize whitespace, decode HTML entities, drop common boilerplate noise."""
    text = html.unescape(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _WS.sub(" ", text)
    text = "\n".join(line.strip() for line in text.split("\n"))
    text = _MULTI_NL.sub("\n\n", text)
    return text.strip()


def html_to_text(raw_html: str, *, drop_selectors: tuple[str, ...] = ()) -> str:
    """Convert HTML to clean text. Removes script/style/nav/footer/header and any
    extra CSS selectors passed in `drop_selectors`."""
    soup = BeautifulSoup(raw_html, "html.parser")
    for tag in soup(["script", "style", "noscript", "nav", "footer", "header",
                     "form", "aside", "iframe", "svg"]):
        tag.decompose()
    for sel in drop_selectors:
        for tag in soup.select(sel):
            tag.decompose()
    text = soup.get_text("\n")
    return clean_text(text)


def header_block(source_id: str, source_name: str, source_url: str) -> str:
    """Standard header prepended to every document file."""
    return (
        f"SOURCE: {source_name}\n"
        f"SOURCE_ID: {source_id}\n"
        f"URL: {source_url}\n"
        f"---\n"
    )


def polite_sleep(seconds: float = 1.0) -> None:
    time.sleep(seconds)
