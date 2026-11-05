#!/usr/bin/env python3
"""Download XHS captions as SRT and plain text to /tmp/xhs_captions by default."""

import argparse
import html
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36"


def normalise_page(text: str) -> str:
    for escaped, literal in ((r"\u002F", "/"), (r"\u0026", "&"),
                             (r"\u003F", "?"), (r"\u003D", "="),
                             (r"\u0025", "%"), (r'\"', '"'), (r"\/", "/")):
        text = text.replace(escaped, literal)
    return html.unescape(text)


def find_subtitle_url(page: str) -> str:
    page = normalise_page(page)
    match = re.search(
        r'"source"\s*:\s*\[\s*\{[^{}]*?"url"\s*:\s*"([^" ]+\.srt(?:\?[^" ]*)?)"',
        page, re.IGNORECASE)
    if match:
        return match.group(1)
    match = re.search(r'https?://sns-subtitle-[^"\s<>]+?\.srt(?:\?[^"\s<>]*)?',
                      page, re.IGNORECASE)
    if match:
        return match.group(0)
    raise RuntimeError("No subtitle track found in the page")


def srt_to_text(srt: str) -> str:
    paragraphs = []
    timestamp = re.compile(r"\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*"
                           r"\d{2}:\d{2}:\d{2}[,.]\d{3}")
    for block in re.split(r"\r?\n\s*\r?\n", srt.strip()):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) > 1 and re.fullmatch(r"\d+", lines[0]) and timestamp.fullmatch(lines[1]):
            lines.pop(0)
        text = [line for line in lines if not timestamp.fullmatch(line)]
        if text:
            paragraphs.append(" ".join(text))
    return "\n".join(paragraphs) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        usage="uv run %(prog)s [--out-dir DIRECTORY] URL")
    parser.add_argument("url", help="XHS short link or full post URL")
    parser.add_argument("--out-dir", default="/tmp/xhs_captions",
                        help="Output directory (default: /tmp/xhs_captions)")
    args = parser.parse_args()
    headers = {"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
               "Accept": "text/html,application/xhtml+xml"}
    try:
        with urlopen(Request(args.url, headers=headers), timeout=30) as response:
            final_url = response.geturl()
            page = response.read().decode("utf-8", errors="replace")
        subtitle_url = find_subtitle_url(page)
        with urlopen(Request(subtitle_url, headers=headers), timeout=30) as response:
            subtitle = response.read().decode("utf-8-sig", errors="replace")
    except (HTTPError, URLError, TimeoutError) as exc:
        print(f"Network error: {exc}", file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(f"Extraction error: {exc}", file=sys.stderr)
        return 2

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    match = re.search(r"/explore/([0-9a-zA-Z]+)", final_url)
    stem = match.group(1) if match else "xhs_note"
    srt_path, txt_path = out_dir / f"{stem}.srt", out_dir / f"{stem}.txt"
    srt_path.write_text(subtitle, encoding="utf-8")
    txt_path.write_text(srt_to_text(subtitle), encoding="utf-8")
    print(f"Final URL: {final_url}")
    print(f"Subtitle URL: {subtitle_url}")
    print(f"Saved: {srt_path}")
    print(f"Saved: {txt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
