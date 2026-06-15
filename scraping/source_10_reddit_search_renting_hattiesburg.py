"""Reddit universal search — cross-subreddit discussions on Hattiesburg renting,
tenant laws, landlord feedback."""
from __future__ import annotations

from .utils import FetchError, clean_text, fetch_json, polite_sleep

SOURCE_ID = "10_reddit_search_renting_hattiesburg"
SOURCE_NAME = "Reddit Universal Search (Hattiesburg renting)"
SOURCE_URL = "https://www.reddit.com/search/?q=renting+hattiesburg"

SEARCH_QUERIES = (
    "renting hattiesburg",
    "tenant rights mississippi",
    "landlord hattiesburg",
    "lease hattiesburg",
    "apartment scam hattiesburg",
)


def _format_post(post: dict) -> str:
    title = post.get("title", "").strip()
    selftext = clean_text(post.get("selftext", "") or "")
    sub = post.get("subreddit", "")
    permalink = post.get("permalink", "")
    score = post.get("score", 0)
    parts = [
        f"### r/{sub}: {title}",
        f"score={score}  url=https://reddit.com{permalink}",
    ]
    if selftext:
        parts.append(selftext)
    return "\n".join(parts)


def scrape() -> str:
    out = []
    seen = set()
    for q in SEARCH_QUERIES:
        url = (
            "https://www.reddit.com/search.json"
            f"?q={q.replace(' ', '+')}&sort=relevance&limit=15&type=link"
        )
        try:
            data = fetch_json(url)
        except FetchError as e:
            out.append(f"[search '{q}' failed: {e}]")
            continue

        children = data.get("data", {}).get("children", [])
        out.append(f"## Search: {q}  ({len(children)} results)\n")
        for child in children:
            post = child.get("data", {})
            pid = post.get("id")
            if not pid or pid in seen:
                continue
            seen.add(pid)
            out.append(_format_post(post))
            out.append("")
        polite_sleep(0.5)

    if not out:
        return "[no posts retrieved]"
    return "\n".join(out)
