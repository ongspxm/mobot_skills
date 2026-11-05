"""DuckDuckGo search for Prime Agent."""

import asyncio

from ddgs import DDGS


async def run(query: str, max_results: int = 15) -> list[dict[str, str | None]]:
    """Search DuckDuckGo and return titles, URLs, and snippets.

    Args:
        query: Search terms.
        max_results: Maximum number of results to return.
    """
    rows = await asyncio.to_thread(
        lambda: DDGS().text(query, max_results=max_results)
    )
    return [
        {"title": r.get("title"), "url": r.get("href"), "snippet": r.get("body")}
        for r in rows
    ]
