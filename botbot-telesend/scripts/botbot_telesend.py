#!/usr/bin/env python3
import argparse
import json
import mimetypes
import os
import sys
import uuid
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class CliError(RuntimeError):
    pass


def _config_path() -> Path:
    botbot_home = os.getenv("BOTBOT_HOME")
    if botbot_home:
        return Path(botbot_home).expanduser() / "botbot-telesend.json"
    return Path.home() / ".botbot" / "botbot-telesend.json"


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise CliError(f"config not found: {path}")
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CliError(f"failed to read config: {path}: {exc}") from exc
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CliError(f"invalid JSON config: {path}: {exc}") from exc


def _require_str(cfg: dict[str, Any], key: str) -> str:
    value = str(cfg.get(key, "")).strip()
    if not value:
        raise CliError(f"missing required config field: {key}")
    return value


def _http_json(req: Request) -> dict[str, Any]:
    try:
        with urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
    except HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise CliError(f"HTTP {exc.code}: {details}") from exc
    except URLError as exc:
        raise CliError(f"network error: {exc}") from exc

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CliError(f"invalid JSON response: {exc}") from exc

    if payload.get("ok") is True:
        return payload

    error_code = payload.get("error_code")
    description = payload.get("description")
    raise CliError(f"telegram api error ({error_code}): {description}")


def _multipart_payload(fields: dict[str, str], files: list[tuple[str, Path]]) -> tuple[bytes, str]:
    boundary = f"----botbot{uuid.uuid4().hex}"
    chunks: list[bytes] = []

    for key, value in fields.items():
        chunks.append(
            (
                f"--{boundary}\r\n"
                f"Content-Disposition: form-data; name=\"{key}\"\r\n\r\n"
                f"{value}\r\n"
            ).encode("utf-8")
        )

    for field_name, path in files:
        mime, _ = mimetypes.guess_type(path.name)
        chunks.append(
            (
                f"--{boundary}\r\n"
                f"Content-Disposition: form-data; name=\"{field_name}\"; filename=\"{path.name}\"\r\n"
                f"Content-Type: {mime or 'application/octet-stream'}\r\n\r\n"
            ).encode("utf-8")
        )
        try:
            chunks.append(path.read_bytes())
        except OSError as exc:
            raise CliError(f"failed to read image: {path}: {exc}") from exc
        chunks.append(b"\r\n")

    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks), boundary


class TelegramClient:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id

    def _url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def _post_json(self, method: str, body: dict[str, Any]) -> dict[str, Any]:
        req = Request(
            url=self._url(method),
            method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            data=json.dumps(body).encode("utf-8"),
        )
        return _http_json(req)

    def _post_multipart(self, method: str, fields: dict[str, str], files: list[tuple[str, Path]]) -> dict[str, Any]:
        payload, boundary = _multipart_payload(fields, files)
        req = Request(
            url=self._url(method),
            method="POST",
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}", "Accept": "application/json"},
            data=payload,
        )
        return _http_json(req)

    def send_text(self, text: str) -> dict[str, Any]:
        return self._post_json("sendMessage", {"chat_id": self.chat_id, "text": text})

    def send_photo(self, img: Path, caption: str | None) -> dict[str, Any]:
        fields = {"chat_id": self.chat_id}
        if caption:
            fields["caption"] = caption
        return self._post_multipart("sendPhoto", fields, [("photo", img)])

    def send_media_group(self, imgs: list[Path], caption: str | None) -> dict[str, Any]:
        media: list[dict[str, str]] = []
        files: list[tuple[str, Path]] = []
        for i, img in enumerate(imgs):
            key = f"file{i}"
            item = {"type": "photo", "media": f"attach://{key}"}
            if i == 0 and caption:
                item["caption"] = caption
            media.append(item)
            files.append((key, img))

        fields = {
            "chat_id": self.chat_id,
            "media": json.dumps(media, separators=(",", ":")),
        }
        return self._post_multipart("sendMediaGroup", fields, files)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="botbot-telesend", description="Tiny Telegram sender")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_send = sub.add_parser("send", help="Send text and optional images")
    text_group = p_send.add_mutually_exclusive_group(required=True)
    text_group.add_argument("--text", help="Message text")
    text_group.add_argument("--textfile", help="Path to UTF-8 text file")
    p_send.add_argument("--img", action="append", default=[], help="Image filename (repeatable)")

    return parser


def _validate_imgs(imgs: list[str]) -> list[Path]:
    paths: list[Path] = []
    for raw in imgs:
        p = Path(raw).expanduser()
        if not p.exists():
            raise CliError(f"image not found: {p}")
        if not p.is_file():
            raise CliError(f"image is not a file: {p}")
        paths.append(p)
    return paths


def _read_text(args: argparse.Namespace) -> str:
    if args.text is not None:
        text = args.text
    else:
        p = Path(args.textfile).expanduser()
        if not p.exists():
            raise CliError(f"text file not found: {p}")
        if not p.is_file():
            raise CliError(f"text file is not a file: {p}")
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise CliError(f"text file is not valid UTF-8: {p}") from exc
        except OSError as exc:
            raise CliError(f"failed to read text file: {p}: {exc}") from exc
    if not text.strip():
        raise CliError("message text is empty")
    return text


def main() -> int:
    args = _build_parser().parse_args()
    cfg_path = _config_path()
    try:
        cfg = _read_json(cfg_path)
        client = TelegramClient(_require_str(cfg, "bottkn"), _require_str(cfg, "chatid"))

        if args.cmd != "send":
            raise CliError(f"unknown command: {args.cmd}")

        text = _read_text(args)
        imgs = _validate_imgs(args.img)
        if not imgs:
            print(json.dumps(client.send_text(text), indent=2))
            return 0

        results: list[dict[str, Any]] = []
        first_batch = True
        for i in range(0, len(imgs), 10):
            batch = imgs[i : i + 10]
            caption = text if first_batch else None
            if len(batch) == 1:
                results.append(client.send_photo(batch[0], caption))
            else:
                results.append(client.send_media_group(batch, caption))
            first_batch = False

        print(
            json.dumps(
                {
                    "ok": True,
                    "chat_id": client.chat_id,
                    "images_sent": len(imgs),
                    "batches": len(results),
                    "results": [item.get("result") for item in results],
                },
                indent=2,
            )
        )
        return 0
    except CliError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
