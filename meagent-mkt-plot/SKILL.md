---
name: meagent-mkt-plot
description: Use when you need daily market charts and a PNG summary table sent to Telegram.
---

# Meagent Market Plot

## Workflow

1. Run the script:

   ```bash
   uv run <path-to-skill>/scripts/meagent_mkt_plot.py run
   ```

2. Send every PNG it makes directly with `botbot-telesend`. Do not send only file paths or links. Put the files in one send when there are 2-10 files:

   ```bash
   uv run <path-to-botbot-telesend>/scripts/botbot_telesend.py send \
     --text "Market plots" \
     --img /tmp/overview.png \
     --img /tmp/<tag>.png
   ```

   For more than 10 files, send batches of 10. Use the real tag file names from the script output.

## Output

- Reads groups from `~/.botbot/meagent-mkt-plot.json`.
- Writes `overview.png` and one PNG per tag to `/tmp`.
- Each tag chart has four panels: `1w`, `4w`, `12w`, and `52w`.
- Each line starts at `100`.
- Each panel has a dotted `100` line, a grid, and a legend outside the plot.
- Legend change windows are `1d`, `1w`, `4w`, and `12w` for the four panels.
- Bad tickers and missing panels are skipped with a warning. The run fails only when no ticker has daily data.

## Configuration

Use a JSON object at `~/.botbot/meagent-mkt-plot.json`:

```json
{
  "benchmarks": ["^GSPC", "^IXIC", "^VIX"],
  "sectors": ["XLK", "XLF", "XLE"],
  "crypto": ["BTC-USD", "ETH-USD", "SOL-USD"],
  "macro": ["^TNX", "DX-Y.NYB", "GC=F"]
}
```

Each key makes one chart. Each list item makes one line.
