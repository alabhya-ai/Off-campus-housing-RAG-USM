"""Uloop — USM campus classifieds (housing listings, subleases, roommates)."""
from .utils import FetchError, clean_text, fetch_html, html_to_text

SOURCE_ID = "07_uloop_usm"
SOURCE_NAME = "Uloop (USM Campus Classifieds)"
SOURCE_URL = "https://usm.uloop.com/housing/"


def scrape() -> str:
    try:
        raw = fetch_html(SOURCE_URL)
    except FetchError as e:
        return f"[fetch failed: {e}]"

    text = html_to_text(
        raw,
        drop_selectors=(
            "#header", "#footer", ".sidebar", ".ad", ".breadcrumbs",
            ".pagination",
        ),
    )
    return clean_text(text)
