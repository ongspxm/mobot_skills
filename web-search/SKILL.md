---
name: web-search
description: Search the web with DuckDuckGo for current information and source links. Use when the user asks about recent events, current prices, external docs, or anything that needs an outside source, and when verifying a claim with links.
---

# Web Search

    Kernel:     await web_search("query", max_results=5)
    Shell:      web_search "query" --max-results 5
    Standalone: uvx --from <skill-dir> web_search "query" --max-results 5

Returns a list of `{"title", "url", "snippet"}` dicts.

## Boundaries

- Results can lag live data. For exact quotes, query the source API.
- Snippets are truncated. Open the URL when exact wording matters.
- No API key, no retry handling. Keep queries specific and few.
- Cite the `url` when reporting a fact.
