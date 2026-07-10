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

Use when you need to search for list of links. Otherwise visit pages directly using curl.

## COMMANDS

`search QUERY`
: Print numbered result titles, URLs, and snippets.

## OPTIONS

`--count N`
: Search results to print. Default: `5`. Maximum: `20`.

## FILES

- Entrypoint: `scripts/web_search.py`
