---
name: meagent-mkt-plot
description: Use when you need daily multi-horizon market comparison charts with normalized lines and CSV summary metrics.
---

# MEAGENT-MKT-PLOT(1)

## NAME

`meagent-mkt-plot` - generate one normalized 4-panel market chart per configured tag and emit a deterministic CSV ticker summary.

## SYNOPSIS

```bash
uv run --with=yfinance --with=matplotlib <path-to-skill>/scripts/meagent_mkt_plot.py run
```

## DESCRIPTION

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

## CONFIG

Config shape is a JSON object mapping `tag -> [tickers...]`.

Path:

- `~/.botbot/meagent-mkt-plot.json`

Example:

```json
{
  "benchmarks": ["^GSPC", "^IXIC", "^VIX"],
  "sectors": ["XLK", "XLF", "XLE"],
  "crypto": ["BTC-USD", "ETH-USD", "SOL-USD"],
  "macro": ["^TNX", "DX-Y.NYB", "GC=F"]
}
```

How to control plotted assets:

- Add/remove a tag key to control chart grouping.
- Add/remove tickers inside each tag array to control plotted lines.
- Rename tag key to change output chart filename prefix.

## EXAMPLES

```bash
# Reads default config path (~/.botbot/meagent-mkt-plot.json)
uv run --with=yfinance --with=matplotlib <path-to-skill>/scripts/meagent_mkt_plot.py run
```
