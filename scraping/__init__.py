"""Scrapers for the 10 sources defined in planning.md.

Each `source_NN_*.py` module exposes:
    SOURCE_ID:   str   — used as the output filename stem (e.g. "01_apartments_com")
    SOURCE_NAME: str   — human-readable name
    SOURCE_URL:  str   — origin URL
    scrape() -> str    — returns cleaned plain text for the document
"""
