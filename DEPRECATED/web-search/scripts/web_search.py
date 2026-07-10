#!/usr/bin/env python3
"""No-key web search helper"""

from __future__ import annotations

import argparse
import html
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36"
DDG_LITE_URL = "https://lite.duckduckgo.com/lite/"
DDG_RESULT_LIMIT = 20
ANCHOR_RE = re.compile(
    r"<a(?P<attrs>[^>]*class=['\"]result-link['\"][^>]*)>(?P<title>.*?)</a>",
    flags=re.S,
)
HREF_RE = re.compile(r"href=['\"]([^'\"]+)['\"]", flags=re.S)
SNIPPET_RE = re.compile(r"class=['\"]result-snippet['\"][^>]*>(.*?)</td>", flags=re.S)


def clean_html_text(text: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", html.unescape(text))
    return re.sub(r"\s+", " ", text).strip()


def parse_ddg_lite_results(page: str) -> list[dict[str, str]]:
    if "Unfortunately, bots use DuckDuckGo too" in page or "anomaly-modal" in page:
        raise RuntimeError("DuckDuckGo anti-bot challenge encountered; retry later")

    anchors = list(ANCHOR_RE.finditer(page))
    results: list[dict[str, str]] = []
    seen: set[str] = set()

    for i, match in enumerate(anchors):
        row_start = page.rfind("<tr", 0, match.start())
        if row_start != -1 and "result-sponsored" in page[row_start : match.start()]:
            continue

        href_match = HREF_RE.search(match.group("attrs"))
        if not href_match:
            continue

        link = html.unescape(href_match.group(1)).strip()
        if link.startswith("//"):
            link = "https:" + link
        uddg = urllib.parse.parse_qs(urllib.parse.urlparse(link).query).get("uddg")
        if uddg and uddg[0]:
            link = urllib.parse.unquote(uddg[0])
        title = clean_html_text(match.group("title"))
        if not title or not link or link in seen:
            continue

        next_start = anchors[i + 1].start() if i + 1 < len(anchors) else len(page)
        snippet_match = SNIPPET_RE.search(page[match.end() : next_start])
        description = clean_html_text(snippet_match.group(1)) if snippet_match else ""

        seen.add(link)
        results.append({"title": title, "link": link, "description": description})
        if len(results) >= DDG_RESULT_LIMIT:
            break

    return results


def request_text(url: str, *, timeout: int = 30) -> tuple[str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read()
        content_type = response.headers.get("content-type", "")
        charset_match = re.search(r"charset=([^;]+)", content_type, flags=re.I)
        charset = charset_match.group(1).strip() if charset_match else "utf-8"
        return raw.decode(charset, errors="replace"), content_type


def search(query: str, *, count: int) -> int:
    query = query.strip()
    if not query:
        print("Error: query must not be empty", file=sys.stderr)
        return 2

    count = min(max(count, 1), DDG_RESULT_LIMIT)
    params = urllib.parse.urlencode({"q": query, "kl": "en-us"})
    page, _ = request_text(f"{DDG_LITE_URL}?{params}", timeout=20)
    results = parse_ddg_lite_results(page)[:count]

    if not results:
        print(f"No results for: {query}")
        return 0

    print(f"Results for: {query}\n")
    for i, item in enumerate(results, 1):
        print(f"{i}. {item['title']}\n   {item['link']}")
        if item.get("description"):
            print(f"   {item['description']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="No-key DuckDuckGo Lite search helper.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search DuckDuckGo Lite")
    search_parser.add_argument("query")
    search_parser.add_argument("--count", type=int, default=5)

    args = parser.parse_args()
    try:
        if args.command == "search":
            return search(args.query, count=args.count)
    except urllib.error.HTTPError as exc:
        print(f"Error: HTTP {exc.code} for {exc.url}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
