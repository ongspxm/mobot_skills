#!/usr/bin/env python3
import argparse
import base64
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


class CliError(RuntimeError):
    pass


@dataclass
class ConfigPaths:
    path: Path

    @staticmethod
    def resolve(explicit_path: str | None) -> "ConfigPaths":
        if explicit_path:
            return ConfigPaths(Path(explicit_path).expanduser())
        botbot_home = os.getenv("BOTBOT_HOME")
        if botbot_home:
            return ConfigPaths(Path(botbot_home).expanduser() / "botbot-gmail.json")
        return ConfigPaths(Path.home() / ".botbot" / "botbot-gmail.json")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise CliError(f"config not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CliError(f"invalid JSON config: {path}: {exc}") from exc


class _TagStripper(HTMLParser):
    BLOCK_TAGS = {"br", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "p", "section", "td", "tr"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.href: str | None = None
        self.ignored = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"style", "script"}:
            self.ignored += 1
        elif not self.ignored:
            if tag in self.BLOCK_TAGS:
                self.parts.append("\n")
            if tag == "a":
                self.href = dict(attrs).get("href")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"style", "script"}:
            self.ignored = max(0, self.ignored - 1)
        elif not self.ignored:
            if tag == "a" and self.href:
                self.parts.append(f" ({self.href})")
                self.href = None
            if tag in self.BLOCK_TAGS:
                self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.ignored:
            self.parts.append(data)

    def text(self) -> str:
        return "".join(self.parts)


class GmailClient:
    def __init__(self, cfg_path: Path):
        cfg = _read_json(cfg_path)
        gog_cfg = cfg.get("gog") if isinstance(cfg.get("gog"), dict) else {}
        self.account = str((gog_cfg or {}).get("account") or cfg.get("account") or "").strip()
        self.client = str((gog_cfg or {}).get("client") or cfg.get("client") or "").strip()

    def _run_gog_json(self, *args: str) -> Any:
        cmd = ["gog", "--json", "--results-only", "--no-input"]
        if self.account:
            cmd.extend(["--account", self.account])
        if self.client:
            cmd.extend(["--client", self.client])
        cmd.extend(args)
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            msg = proc.stderr.strip() or proc.stdout.strip() or f"gog failed: {' '.join(cmd)}"
            raise CliError(msg)
        payload = proc.stdout.strip()
        if not payload:
            return {}
        try:
            return json.loads(payload)
        except json.JSONDecodeError as exc:
            raise CliError(f"invalid JSON from gog: {exc}") from exc

    @staticmethod
    def _latest_message(thread: dict[str, Any]) -> dict[str, Any]:
        messages = thread.get("messages")
        if not isinstance(messages, list) or not messages:
            raise CliError("thread has no messages")

        def internal_date(message: Any) -> int:
            if not isinstance(message, dict):
                return 0
            try:
                return int(str(message.get("internalDate", message.get("internal_date", 0))) or 0)
            except ValueError:
                return 0

        latest = max(messages, key=internal_date)
        if not isinstance(latest, dict):
            raise CliError("unexpected message response from gog")
        return latest

    @staticmethod
    def _decode_b64url(raw: str) -> str:
        try:
            data = raw.strip()
            padding = "=" * ((4 - len(data) % 4) % 4)
            return base64.urlsafe_b64decode((data + padding).encode()).decode("utf-8", errors="ignore")
        except Exception:
            return ""

    def _extract_body_part(self, payload: dict[str, Any], mime: str) -> str:
        if payload.get("mimeType") == mime:
            return self._decode_b64url(str((payload.get("body") or {}).get("data", "")))
        for part in payload.get("parts") or []:
            if isinstance(part, dict):
                text = self._extract_body_part(part, mime)
                if text:
                    return text
        return ""

    def _plaintext(self, message: dict[str, Any]) -> str:
        payload = message.get("payload")
        if isinstance(payload, dict):
            html_part = self._extract_body_part(payload, "text/html")
            if html_part:
                stripper = _TagStripper()
                stripper.feed(html_part)
                return stripper.text()
            plain = self._extract_body_part(payload, "text/plain")
            if plain:
                return plain
        for key in ("textBody", "text", "body"):
            value = message.get(key)
            if isinstance(value, str) and value.strip():
                return value
        return str(message.get("snippet", ""))

    @staticmethod
    def _labels(value: Any) -> list[str]:
        if not isinstance(value, list):
            return []
        return [str(x.get("name") or x.get("id") or "") if isinstance(x, dict) else str(x) for x in value if str(x)]

    def list_threads(self, query: str) -> list[dict[str, Any]]:
        data = self._run_gog_json("gmail", "search", query, "--all", "--max", "100")
        if not isinstance(data, list):
            return []
        rows: list[dict[str, Any]] = []
        for item in data:
            if not isinstance(item, dict):
                continue
            threadid = str(item.get("threadId") or item.get("thread_id") or item.get("id") or "").strip()
            if not threadid:
                continue
            rows.append(
                {
                    "threadid": threadid,
                    "from": str(item.get("from") or item.get("sender") or ""),
                    "reply-to": str(
                        item.get("replyTo") or item.get("reply_to") or item.get("reply-to") or ""
                    ),
                    "subject": str(item.get("subject") or ""),
                    "tstamp": item.get("internalDate") or item.get("internal_date") or item.get("date") or "",
                    "labels": self._labels(item.get("labels") or item.get("labelIds")),
                }
            )
        return rows

    def delete_thread(self, thread_id: str) -> dict[str, str]:
        tid = thread_id.strip()
        if not tid:
            raise CliError("threadid cannot be empty")
        self._run_gog_json("gmail", "thread", "modify", tid, "--add", "TRASH")
        return {"threadid": tid, "status": "trashed"}

    def read_latest_thread_body(self, thread_id: str) -> str:
        tid = thread_id.strip()
        if not tid:
            raise CliError("threadid cannot be empty")
        data = self._run_gog_json("gmail", "thread", "get", tid, "--full")
        if not isinstance(data, dict):
            raise CliError("unexpected response from gog gmail thread get")
        thread = data.get("thread") if isinstance(data.get("thread"), dict) else data
        text = self._plaintext(self._latest_message(thread)).strip()
        if not text:
            raise CliError("unable to extract body from latest message")
        return text

    def modify_thread_label(self, thread_id: str, label: str, flag: str) -> dict[str, Any]:
        tid = thread_id.strip()
        name = label.strip()
        if not tid:
            raise CliError("threadid cannot be empty")
        if not name:
            raise CliError("label cannot be empty")
        data = self._run_gog_json("gmail", "thread", "modify", tid, flag, name)
        labels = self._labels(data.get("labels") or data.get("labelIds")) if isinstance(data, dict) else []
        action = "added_label" if flag == "--add" else "removed_label"
        return {"threadid": tid, action: name, "labels": labels}

    def refresh_access_token(self) -> dict[str, str]:
        self._run_gog_json("auth", "list", "--check")
        return {"status": "ok"}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="botbot-gmail", description="Tiny Gmail CLI")
    parser.add_argument("--config", help="Path to botbot-gmail.json config")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("refresh", help="Verify gog can refresh the configured account token")
    p_ls = sub.add_parser("ls", help='List threads matching query (default: "in:INBOX")')
    p_ls.add_argument("query", nargs="?", default="in:INBOX")
    for cmd, help_text in (("del", "Trash a thread by id"), ("read", "Read latest body with inline links")):
        item = sub.add_parser(cmd, help=help_text)
        item.add_argument("threadid", help="Gmail thread id")
    for cmd, help_text in (("tag", "Add label to a thread"), ("untag", "Remove label from a thread")):
        item = sub.add_parser(cmd, help=help_text)
        item.add_argument("threadid", help="Gmail thread id")
        item.add_argument("label", help="Label name or id")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        client = GmailClient(ConfigPaths.resolve(args.config).path)
        if args.cmd == "refresh":
            print(json.dumps(client.refresh_access_token(), indent=2))
        elif args.cmd == "ls":
            for row in client.list_threads(args.query):
                print(json.dumps(row, separators=(",", ":")))
        elif args.cmd == "del":
            print(json.dumps(client.delete_thread(args.threadid), indent=2))
        elif args.cmd == "read":
            print(client.read_latest_thread_body(args.threadid))
        elif args.cmd == "tag":
            print(json.dumps(client.modify_thread_label(args.threadid, args.label, "--add"), indent=2))
        elif args.cmd == "untag":
            print(json.dumps(client.modify_thread_label(args.threadid, args.label, "--remove"), indent=2))
        return 0
    except CliError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
