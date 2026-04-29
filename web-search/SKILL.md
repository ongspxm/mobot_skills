---
name: web-search
description: Use for no-key DuckDuckGo Lite search.
---

# WEB-SEARCH(1)

## NAME

`web-search` - no-key web search helper.

## SYNOPSIS

```bash
uv run <path-to-skill>/scripts/web_search.py search "query"
uv run <path-to-skill>/scripts/web_search.py search "query" --count 20
```

## DESCRIPTION

Searches DuckDuckGo Lite with the `en-US` locale and no API key. Use it when a task needs public web results or links.

Always run with `uv run`. For ordinary direct URL fetches, `curl` is usually fine; during web-search tasks, use this tool for search results.

## COMMANDS

`search QUERY`
: Print numbered result titles, URLs, and snippets.

## OPTIONS

`--count N`
: Search results to print. Default: `5`. Maximum: `20`.

## FILES

- Entrypoint: `scripts/web_search.py`
