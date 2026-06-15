"""ForRentUniversity — USM portal with walk-time-to-campus listings."""
from .utils import FetchError, clean_text, fetch_html, html_to_text

SOURCE_ID = "09_forrentuniversity_usm"
SOURCE_NAME = "ForRentUniversity (USM Portal)"
SOURCE_URL = "https://www.forrentuniversity.com/The-University-of-Southern-Mississippi"


def scrape() -> str:
    try:
        raw = fetch_html(SOURCE_URL)
    except FetchError as e:
        return f"[fetch failed: {e}]"

    text = html_to_text(
        raw,
        drop_selectors=(
            ".header", ".footer", ".nav", ".cookie-banner", ".advertisement",
        ),
    )
    return clean_text(text)
