"""Run every scraper in scraping/ and write its output to documents/.

Usage:
    python scrape.py              # run all 10 sources
    python scrape.py 5 6 10       # run only sources 5, 6, 10
"""
from __future__ import annotations

import importlib
import sys
import traceback
from pathlib import Path

from scraping.utils import header_block
from config import DOCUMENTS_DIR

SOURCE_MODULES = [
    "scraping.source_01_apartments_com",
    "scraping.source_02_zillow",
    "scraping.source_03_collegerentals",
    "scraping.source_04_rent_com",
    "scraping.source_05_reddit_hattiesburg",
    "scraping.source_06_reddit_southernmiss",
    "scraping.source_07_uloop",
    "scraping.source_08_usm_offcampus_portal",
    "scraping.source_09_forrentuniversity",
    "scraping.source_10_reddit_search_renting_hattiesburg",
]


def _selected_modules(argv: list[str]) -> list[str]:
    if not argv:
        return SOURCE_MODULES
    wanted = {int(a) for a in argv}
    return [m for m in SOURCE_MODULES if int(m.split("_")[1][:2]) in wanted]


def run_one(module_name: str, out_dir: Path) -> tuple[str, str, int]:
    mod = importlib.import_module(module_name)
    sid = mod.SOURCE_ID
    name = mod.SOURCE_NAME
    url = mod.SOURCE_URL
    try:
        body = mod.scrape()
    except Exception as e:
        body = f"[scraper crashed: {e!r}]\n{traceback.format_exc()}"
    out_path = out_dir / f"{sid}.txt"
    full = header_block(sid, name, url) + body.strip() + "\n"
    out_path.write_text(full, encoding="utf-8")
    return sid, str(out_path), len(full)


def main(argv: list[str]) -> int:
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    modules = _selected_modules(argv)
    print(f"Scraping {len(modules)} source(s) -> {DOCUMENTS_DIR}\n")
    for m in modules:
        try:
            sid, path, n = run_one(m, DOCUMENTS_DIR)
            print(f"  [{sid}] wrote {n:>7} chars -> {path}")
        except Exception as e:
            print(f"  [{m}] FAILED to write: {e!r}")
    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
