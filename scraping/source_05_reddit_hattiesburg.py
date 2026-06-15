"""r/hattiesburg — community subreddit, search for housing-related threads."""
from __future__ import annotations

from .utils import FetchError, clean_text, fetch_json, polite_sleep

SOURCE_ID = "05_reddit_hattiesburg"
SOURCE_NAME = "r/hattiesburg Subreddit"
SOURCE_URL = "https://www.reddit.com/r/hattiesburg/"

SEARCH_QUERIES = (
    "USM apartment",
    "moving here apartment",
    "apartment suggestion",
    "rent Hattiesburg",
    "pet friendly apartment",
)


def _format_post(post: dict) -> str:
    title = post.get("title", "").strip()
    selftext = clean_text(post.get("selftext", "") or "")
    permalink = post.get("permalink", "")
    score = post.get("score", 0)
    num_comments = post.get("num_comments", 0)
    parts = [
        f"### {title}",
        f"score={score}  comments={num_comments}  url=https://reddit.com{permalink}",
    ]
    if selftext:
        parts.append(selftext)
    return "\n".join(parts)


def _fetch_comments(permalink: str) -> str:
    """Pull top-level comment bodies from a post's JSON listing."""
    url = f"https://www.reddit.com{permalink}.json?limit=20&depth=1"
    try:
        data = fetch_json(url)
    except FetchError:
        return ""
    if not isinstance(data, list) or len(data) < 2:
        return ""
    comments = data[1].get("data", {}).get("children", [])
    bodies = []
    for c in comments:
        if c.get("kind") != "t1":
            continue
        body = clean_text(c.get("data", {}).get("body", "") or "")
        if body and not body.startswith("[removed]") and not body.startswith("[deleted]"):
            bodies.append(f"- {body}")
    return "\n".join(bodies)


def scrape() -> str:
    out = []
    seen = set()
    for q in SEARCH_QUERIES:
        url = (
            "https://www.reddit.com/r/hattiesburg/search.json"
            f"?q={q.replace(' ', '+')}&restrict_sr=1&sort=relevance&limit=10"
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
            comments = _fetch_comments(post.get("permalink", ""))
            if comments:
                out.append("Top comments:")
                out.append(comments)
            out.append("")
            polite_sleep(0.5)
        polite_sleep(0.5)

    if not out:
        return "[no posts retrieved]"
    return "\n".join(out)
