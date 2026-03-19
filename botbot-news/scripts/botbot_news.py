#!/usr/bin/env python3
import argparse
import email.utils
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from xml.etree import ElementTree as ET


DEFAULT_TIMEOUT_SECONDS = 20
GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q=when:24h%20allinurl:{domain}&hl=en-US&gl=US&ceid=US:en"
SOURCES = [("Reuters", "reuters.com"), ("Bloomberg", "bloomberg.com"), ("FT", "ft.com"), ("WSJ", "wsj.com")]
DEFAULT_FEEDS = [(name, GOOGLE_NEWS_RSS.format(domain=domain)) for name, domain in SOURCES]


class CliError(RuntimeError):
    pass


def _parse_entries(xml_bytes: bytes) -> list[dict[str, str]]:
    root = ET.fromstring(xml_bytes)
    channel = root.find("channel")
    if channel is None:
        raise CliError("unsupported feed format")
    items: list[dict[str, str]] = []
    for node in channel.findall("item"):
        title = (node.findtext("title") or "").strip()
        link = (node.findtext("link") or "").strip()
        published = (node.findtext("pubDate") or "").strip()
        items.append({"title": title, "link": link, "published": published})
    return items


def _fetch_feed(url: str, timeout_seconds: int) -> bytes:
    try:
        with urlopen(url, timeout=timeout_seconds) as resp:
            return resp.read()
    except HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise CliError(f"HTTP {exc.code} for {url}: {details}") from exc
    except URLError as exc:
        raise CliError(f"network error for {url}: {exc}") from exc


def _sort_key(value: str) -> datetime:
    raw = value.strip()
    if not raw:
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        dt = email.utils.parsedate_to_datetime(raw)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return datetime.min.replace(tzinfo=timezone.utc)


def main() -> int:
    argparse.ArgumentParser(
        prog="botbot-news",
        description="Print market headlines from Reuters, Bloomberg, FT, and WSJ",
    ).parse_args()
    try:
        entries: list[dict[str, str]] = []
        seen: set[str] = set()
        failures: list[str] = []
        for source, feed_url in DEFAULT_FEEDS:
            try:
                feed_entries = _parse_entries(_fetch_feed(feed_url, DEFAULT_TIMEOUT_SECONDS))
            except (CliError, ET.ParseError, ValueError) as exc:
                failures.append(f"{source}: {exc}")
                continue

            for item in feed_entries:
                dedupe_key = item["link"].strip().lower() or (
                    f"{item['title'].strip().lower()}|{item['published'].strip().lower()}"
                )
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)
                entries.append(item)

        if not entries:
            if failures:
                print(f"error: unable to fetch any feed ({'; '.join(failures)})", file=sys.stderr)
                return 2
            print("No news items found.")
            return 0

        if failures:
            print(f"warning: some feeds failed ({'; '.join(failures)})", file=sys.stderr)

        entries.sort(key=lambda item: _sort_key(item["published"]), reverse=True)
        for item in entries:
            title = item["title"] or "(no title)"
            print(title)
        return 0
    except (CliError, ET.ParseError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
