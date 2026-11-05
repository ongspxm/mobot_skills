---
name: xhs-captions
description: Download Xiaohongshu subtitle tracks as SRT and plain text. Use when the user asks to extract captions or transcripts from an XHS post URL.
---

# XHS Captions

## Overview

Run the bundled standard-library script on a public XHS URL. It follows redirects and saves the first embedded XHS subtitle track as `.srt` and `.txt` files under `/tmp/xhs_captions`.

## Workflow

1. Run `uv run <path-to-skill>/script.py URL`.
2. Pass `--out-dir DIRECTORY` to override the default `/tmp/xhs_captions` output directory.
3. Report the final URL, subtitle URL, and saved paths printed by the script.

Example:

```sh
uv run <path-to-skill>/script.py 'https://www.xiaohongshu.com/explore/POST_ID' --out-dir transcripts
```

## Boundaries

- The script downloads captions embedded in the public page; it does not perform speech recognition.
- A network failure exits with status 1. A missing subtitle track exits with status 2.
