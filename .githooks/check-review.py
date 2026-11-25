#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
import os
import pathlib
import re
import subprocess
import sys

ASCII_SKIP_PREFIXES = ("DEPRECATED/", "pstack/", "meagent/meagent-iching/")
CONFLICT_RE = re.compile(r"^(<{7} |={7}$|>{7} )")
PY_DEBUG_RE = re.compile(r"\b(breakpoint|i?pdb\.set_trace)\s*\(")
JS_DEBUG_RE = re.compile(r"^\s*debugger\s*;?\s*$")
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def git(root: pathlib.Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True)


def main() -> int:
    # Find the repository root and files to check.
    root = pathlib.Path(
        subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()
    ).resolve()
    raw_args = sys.argv[1:]

    if raw_args:
        targets = []
        for arg in raw_args:
            p = pathlib.Path(arg)
            resolved = (p if p.is_absolute() else (pathlib.Path.cwd() / p)).resolve()
            try:
                targets.append(resolved.relative_to(root).as_posix())
            except ValueError:
                targets.append(arg)
    else:
        targets = [
            line
            for line in git(
                root, "diff", "--cached", "--name-only", "--diff-filter=ACMR"
            ).splitlines()
            if line
        ]

    errors: list[str] = []
    # Build staged status once so DEPRECATED/ edits are easy to reject.
    allow_deprecated = os.environ.get("ALLOW_DEPRECATED_EDIT") == "1"
    staged_status: dict[str, str] = {}
    if not allow_deprecated:
        for line in git(
            root,
            "diff",
            "--cached",
            "--no-renames",
            "--name-status",
        ).splitlines():
            status, rel = line.split("\t", 1)
            staged_status[rel] = status

    for rel in targets:
        # Reject modified or deleted files in DEPRECATED/.
        if (
            not allow_deprecated
            and rel.startswith("DEPRECATED/")
            and staged_status.get(rel, "").startswith(("M", "D"))
        ):
            errors.append(
                f"{rel}: DEPRECATED/ is read-only "
                "(set ALLOW_DEPRECATED_EDIT=1 to override)"
            )

        path = root / rel
        if not path.is_file():
            continue
        raw = path.read_bytes()
        if b"\x00" in raw:
            continue
        text = raw.decode("utf-8", errors="replace")
        lines = text.splitlines()

        # Reject non-ASCII text outside approved prefixes.
        if not rel.startswith(ASCII_SKIP_PREFIXES):
            for idx, line in enumerate(lines, 1):
                for col, ch in enumerate(line, 1):
                    if ord(ch) > 127:
                        errors.append(
                            f"{rel}:{idx}:{col}: non-ASCII character (U+{ord(ch):04X})"
                        )
                        break

        # Reject merge and debug residue.
        for idx, line in enumerate(lines, 1):
            if CONFLICT_RE.match(line):
                errors.append(f"{rel}:{idx}: merge conflict marker")
            if path.suffix == ".py" and PY_DEBUG_RE.search(line):
                errors.append(f"{rel}:{idx}: debug residue")
            if path.suffix in {".js", ".ts", ".jsx", ".tsx"} and JS_DEBUG_RE.match(
                line
            ):
                errors.append(f"{rel}:{idx}: debugger statement")

        # Validate SKILL.md frontmatter and spong skill names.
        if path.name == "SKILL.md" and not rel.startswith(("DEPRECATED/", "pstack/")):
            frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            if not frontmatter:
                errors.append(f"{rel}:1: missing YAML frontmatter")
                continue

            fields = {}
            for field in frontmatter.group(1).splitlines():
                if ":" in field:
                    key, value = field.split(":", 1)
                    fields[key.strip()] = value.strip()

            name = fields.get("name", "")
            if not name:
                errors.append(f"{rel}:1: frontmatter missing name")
            if not fields.get("description", ""):
                errors.append(f"{rel}:1: frontmatter missing description")
            if rel.startswith("spong/"):
                if not KEBAB_RE.match(name):
                    errors.append(f"{rel}:1: skill name {name!r} must be kebab-case")
                if name != path.parent.name:
                    errors.append(
                        f"{rel}:1: skill name {name!r} != dir {path.parent.name!r}"
                    )

        # Validate spong-mode playbook and principle links.
        if rel == "spong/spong-mode/SKILL.md":
            for pb in re.findall(r"playbooks/([a-z0-9-]+\.md)", text):
                if not (root / "spong" / "spong-mode" / "playbooks" / pb).is_file():
                    errors.append(f"{rel}: missing playbook playbooks/{pb}")
            for idx, line in enumerate(lines, 1):
                match = re.match(r"^- ([a-z0-9-]+): ", line)
                if (
                    match
                    and not (
                        root / "spong" / f"principle-{match.group(1)}" / "SKILL.md"
                    ).is_file()
                ):
                    errors.append(
                        f"{rel}:{idx}: missing principle-{match.group(1)}/SKILL.md"
                    )

    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
