"""Rent.com — Hattiesburg apartments."""
from .utils import FetchError, clean_text, fetch_html, html_to_text

SOURCE_ID = "04_rent_com_hattiesburg"
SOURCE_NAME = "Rent.com (Hattiesburg Apartments)"
SOURCE_URL = "https://www.rent.com/mississippi/hattiesburg-apartments"


def scrape() -> str:
    try:
        raw = fetch_html(SOURCE_URL)
    except FetchError as e:
        return f"[fetch failed: {e}]"

    text = html_to_text(
        raw,
        drop_selectors=(
            ".cookie-banner", ".global-footer", ".global-header",
            ".search-filters", "[class*='Banner']",
        ),
    )
    return clean_text(text)
