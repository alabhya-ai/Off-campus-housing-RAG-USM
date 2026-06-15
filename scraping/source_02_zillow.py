"""Zillow — Hattiesburg rentals."""
from .utils import FetchError, clean_text, fetch_html, html_to_text

SOURCE_ID = "02_zillow_hattiesburg"
SOURCE_NAME = "Zillow (Hattiesburg Rentals)"
SOURCE_URL = "https://www.zillow.com/hattiesburg-ms/rentals/"


def scrape() -> str:
    try:
        raw = fetch_html(SOURCE_URL)
    except FetchError as e:
        return f"[fetch failed: {e}]\nZillow blocks most scraping via Press-and-Hold captcha."

    text = html_to_text(
        raw,
        drop_selectors=(
            "[data-testid='nav']", ".SearchPageListHeader", ".footer-container",
        ),
    )
    return clean_text(text)
