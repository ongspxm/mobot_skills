---
name: meagent-mkt-plot
description: Use when you need daily multi-horizon market comparison charts with normalized lines and CSV summary metrics.
---

# Meagent Market Plot

## Workflows
```bash
uv run --with=yfinance --with=matplotlib <path-to-skill>/scripts/meagent_mkt_plot.py run
```

## When to Use
- Reads groups from `~/.botbot/meagent-mkt-plot.json`.
- Generates one PNG chart per tag/group in `/tmp`.
- Each chart has 4 subplots: `1w`, `4w`, `12w`, `52w`.
- Each subplot uses normalized series starting at `100`.
- Each subplot includes dotted baseline at `100` and visible grid.
- Legends are outside the plot area.
- Legend format: `TICKER (1d +1.2%)` (window token changes by panel).
- Legend change window mapping:
  - `1w` panel -> `1d`
  - `4w` panel -> `1w`
  - `12w` panel -> `4w`
  - `52w` panel -> `12w`
- Stdout is strict CSV only with one stable schema:
  - `ticker,price,pct_1d,pct_1w,pct_4w,pct_12w,pct_52w,vol_ann`
- Non-tabular events/warnings are printed to stderr.
- Partial failure tolerant:
  - bad ticker data is skipped with warning
  - missing panel/window data is skipped with warning
  - run fails only when no ticker has valid daily data

## Configuration
JSON `tag -> [tickers...]` at `~/.botbot/meagent-mkt-plot.json`.

Example:

```json
{
  "benchmarks": ["^GSPC", "^IXIC", "^VIX"],
  "sectors": ["XLK", "XLF", "XLE"],
  "crypto": ["BTC-USD", "ETH-USD", "SOL-USD"],
  "macro": ["^TNX", "DX-Y.NYB", "GC=F"]
}
```

Add/remove tags for chart groups and tickers for lines; rename a tag to change its output filename prefix.

## Examples
```bash
uv run --with=yfinance --with=matplotlib <path-to-skill>/scripts/meagent_mkt_plot.py run
```
