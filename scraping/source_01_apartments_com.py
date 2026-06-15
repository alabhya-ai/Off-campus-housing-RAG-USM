"""Apartments.com — USM off-campus housing listings."""
from .utils import FetchError, clean_text, fetch_html, html_to_text

SOURCE_ID = "01_apartments_com"
SOURCE_NAME = "Apartments.com (USM Off-Campus)"
SOURCE_URL = (
    "https://www.apartments.com/off-campus-housing/ms/hattiesburg/"
    "the-university-of-southern-mississippi/"
)


def scrape() -> str:
    try:
        raw = fetch_html(SOURCE_URL)
    except FetchError as e:
        return f"[fetch failed: {e}]\nApartments.com aggressively blocks unauthenticated scraping."

    text = html_to_text(
        raw,
        drop_selectors=(
            ".cookieBanner", ".footerSection", ".headerSection",
            ".advertisement", ".searchResultsHeader",
        ),
    )
    return clean_text(text)
