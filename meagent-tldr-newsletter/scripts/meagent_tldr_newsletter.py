#!/usr/bin/env python3
import argparse
import json
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit


TLDR_QUERY = "in:INBOX label:6.auto"
TARGET_CHARS = 140
PENDING_PATH = Path("/tmp/meagent_tldr_newsletter_threads.json")
WS_RE = re.compile(r"\s+")
URL_RE = re.compile(r"https?://[^)\s]+")


class CliError(RuntimeError):
    pass


def _gmail_cmd() -> list[str]:
    script = Path(__file__).resolve().parents[2] / "botbot-gmail" / "scripts" / "botbot_gmail.py"
    if not script.is_file():
        raise CliError("required dependency not installed: botbot-gmail")
    return ["uv", "run", str(script)]


def _run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode:
        raise CliError(proc.stderr.strip() or proc.stdout.strip() or f"subprocess failed: {' '.join(cmd)}")
    return proc.stdout


def _shorten(value: str) -> str:
    value = WS_RE.sub(" ", value).strip()
    value = "".join(c if ord(c) < 128 else "_" for c in value)
    if len(value) > TARGET_CHARS:
        return value[: TARGET_CHARS - 3].rstrip() + "..."
    return value


def _format_item(title: str, desc: str, link: str) -> tuple[str, str]:
    # TLDR uses both tracking.tldrnewsletter.com and Short.io links.tldrnewsletter.com.
    parts = urlsplit(link)
    if parts.netloc.lower() == "tracking.tldrnewsletter.com" and parts.path.startswith("/CL0/"):
        encoded_target = parts.path.removeprefix("/CL0/").split("/1/", 1)
        if len(encoded_target) == 2:
            link = unquote(encoded_target[0])
    result = subprocess.run(
        ["curl", "-sS", "-L", "-o", "/dev/null", "-w", "%{url_effective}", "--max-time", "20", link],
        capture_output=True, text=True, check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        link = result.stdout.strip()
    parts = urlsplit(link)
    query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True)
             if not key.startswith("utm_") and key != "ref"]
    link = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
    text = f"=== {_shorten(title)} ({link})\n{_shorten(desc.removeprefix('TL;DR:'))}"
    return link, text


def _parse_tldr(body: str) -> list[tuple[str, str, str]]:
    main, _, rest = body.partition("\nLinks:")
    lines = [line.strip() for line in main.splitlines()]
    items: list[tuple[str, str, str]] = []

    links = {
        int(match.group(1)): match.group(2)
        for line in rest.splitlines()
        if (match := re.match(r"\[(\d+)\]\s+(https?://\S+)", line))
    }

    old_lines = [
        "".join(c if ord(c) < 128 else "_" for c in block.replace("\n", " ").strip())
        for block in main.split("\n\n")
        if block.strip()
    ]
    for line, desc in zip(old_lines, old_lines[1:]):
        token = line.rsplit(" ", 1)[-1]
        if line == line.upper() and re.fullmatch(r"\[\d+\]", token):
            link = links.get(int(token[1:-1]))
            if link:
                items.append((line, desc, link))

    for index, line in enumerate(lines):
        if not re.search(r"\((?:\d+ minute read|GitHub Repo)\)(?: \(sponsor\))?$", line, re.IGNORECASE):
            continue
        values = [value for value in lines[index + 1 :] if value][:2]
        if len(values) == 2 and (match := URL_RE.fullmatch(values[0].strip("()"))):
            items.append((line, values[1], match.group(0)))
    return items


def _parse_aisecret(body: str) -> list[tuple[str, str, str]]:
    lines = [line.strip() for line in body.splitlines()]
    items: list[tuple[str, str, str]] = []
    for index, line in enumerate(lines):
        if line.startswith("TL;DR:") and (
            match := re.search(r"Read more\s*(?:\u2192|->)\s*\((https?://[^)\s]+)\)", line)
        ):
            title = next(
                (value for value in reversed(lines[:index])
                 if value and not URL_RE.fullmatch(value.strip("()"))),
                "",
            )
            if title:
                items.append((title, line.split("Read more", 1)[0].rstrip(), match.group(1)))

    for index, line in enumerate(lines):
        if not URL_RE.fullmatch(line.strip("()")):
            continue
        title = next((value for value in reversed(lines[:index]) if value), "")
        desc = next((value for value in lines[index + 1 :] if value), "")
        if title and "What's happening:" in desc:
            items.append((title, desc, line.strip("()")))

    sections: list[tuple[int, int]] = []
    for index, line in enumerate(lines):
        if not re.fullmatch(r"[A-Z]+", line):
            continue
        title_index = index + 1
        while title_index < len(lines) and not lines[title_index]:
            title_index += 1
        if title_index < len(lines):
            sections.append((index, title_index))

    for position, (index, title_index) in enumerate(sections):
        end = sections[position + 1][0] if position + 1 < len(sections) else len(lines)
        title = lines[title_index]
        candidates = lines[title_index + 1 : end]
        link_index = next(
            (index for index, candidate in enumerate(candidates) if URL_RE.fullmatch(candidate.strip("()"))),
            -1,
        )
        if link_index < 0:
            continue
        desc = candidates[link_index + 1] if link_index + 1 < len(candidates) else ""
        if not desc:
            desc = next((candidate for candidate in reversed(candidates[:link_index]) if candidate), "")
        if "What's happening:" not in desc:
            items.append((title, desc, candidates[link_index].strip("()")))
    return items


def cmd_read(_: argparse.Namespace) -> int:
    if shutil.which("curl") is None:
        raise CliError("required dependency not installed: curl")
    gmail = _gmail_cmd()
    rows = []
    for line in _run(gmail + ["ls", TLDR_QUERY]).splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise CliError("botbot-gmail ls returned non-NDJSON output") from exc
        if isinstance(row, dict):
            rows.append(row)
    rows.sort(key=lambda row: datetime.fromisoformat(str(row["tstamp"])).timestamp(), reverse=True)

    tids: list[str] = []
    items: dict[str, str] = {}
    for row in rows:
        tid = str(row.get("threadid") or "").strip()
        if not tid:
            continue
        sender = str(row.get("from") or "").lower()
        try:
            result = json.loads(_run(gmail + ["read", tid]))
        except json.JSONDecodeError as exc:
            raise CliError("botbot-gmail read returned non-JSON output") from exc
        if not isinstance(result, dict):
            raise CliError("botbot-gmail read returned a non-object")
        body = str(result.get("body") or "")
        if "dan@tldrnewsletter.com" in sender:
            parser = _parse_tldr
        else:
            headers = result.get("headers") if isinstance(result.get("headers"), dict) else {}
            reply_to = str(headers.get("reply-to") or "").lower()
            # Leo sends AI Secret, Robotics Herald, Marketing Secret, and Bay Area Letters.
            if "leo@aisecret.us" not in reply_to:
                continue
            parser = _parse_aisecret
        parsed = parser(body)
        if not parsed:
            continue
        if tid not in tids:
            tids.append(tid)
        with ThreadPoolExecutor(max_workers=128) as executor:
            for key, text in executor.map(lambda item: _format_item(*item), parsed):
                items[key] = text
    PENDING_PATH.write_text(json.dumps({"thread_ids": tids}, separators=(",", ":")), encoding="utf-8")
    if items:
        print("\n\n".join(items.values()) + "\n\nNEXT: if user says ok, read skill and run trash")
    else:
        print("no newsletter found")
    return 0


def cmd_trash(_: argparse.Namespace) -> int:
    if not PENDING_PATH.exists():
        raise CliError("no confirmed newsletter batch found; run read first, show raw output, wait for 'ok'")
    try:
        payload = json.loads(PENDING_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CliError(f"invalid pending batch file: {PENDING_PATH}") from exc
    raw_ids = payload.get("thread_ids") if isinstance(payload, dict) else None
    if not isinstance(raw_ids, list):
        raise CliError(f"invalid pending batch schema: {PENDING_PATH}")
    tids, seen = [], set()
    for raw in raw_ids:
        tid = str(raw).strip()
        if tid and tid not in seen:
            seen.add(tid)
            tids.append(tid)
    if not tids:
        raise CliError("pending newsletter batch is empty; run read again")

    gmail = _gmail_cmd()
    for tid in tids:
        _run(gmail + ["del", tid])
    PENDING_PATH.unlink(missing_ok=True)
    print(json.dumps({"status": "newsletter read and trashed", "count": len(tids)}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Read TLDR newsletters and trash confirmed batch")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("read").set_defaults(func=cmd_read)
    sub.add_parser("trash").set_defaults(func=cmd_trash)
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except CliError as exc:
        print(f"[ERR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
