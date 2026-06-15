"""USM Off-Campus Housing Portal — university/Apartments.com partnership."""
from .utils import FetchError, clean_text, fetch_html, html_to_text

SOURCE_ID = "08_usm_offcampus_portal"
SOURCE_NAME = "USM Off-Campus Housing Portal"
SOURCE_URL = "https://www.usmoffcampushousing.com/housing"


def scrape() -> str:
    try:
        raw = fetch_html(SOURCE_URL)
    except FetchError as e:
        return f"[fetch failed: {e}]"

    text = html_to_text(
        raw,
        drop_selectors=(
            ".site-header", ".site-footer", ".cookie-notice",
            "#mobileNav", ".nav-primary",
        ),
    )
    return clean_text(text)
