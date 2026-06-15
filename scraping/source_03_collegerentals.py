"""CollegeRentals — Hattiesburg student-friendly listings."""
from .utils import FetchError, clean_text, fetch_html, html_to_text

SOURCE_ID = "03_collegerentals_hattiesburg"
SOURCE_NAME = "CollegeRentals (Hattiesburg)"
SOURCE_URL = "https://www.collegerentals.com/off-campus-housing/ms/hattiesburg/"


def scrape() -> str:
    try:
        raw = fetch_html(SOURCE_URL)
    except FetchError as e:
        return f"[fetch failed: {e}]"

    text = html_to_text(
        raw,
        drop_selectors=(".cookieBanner", ".footerSection", ".headerSection"),
    )
    return clean_text(text)
