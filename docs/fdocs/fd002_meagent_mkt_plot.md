---
title: "meagent mkt plot"
active: true
planned: ""
closed: ""
notes: "User requested fdocs only (no implementation code yet)."
---

## Problem

Create a daily long-term market tracking chart generator for Meagent.

- Priority: High
- Effort: Medium (1-4 hours)
- Impact: Gives a consistent daily macro/markets snapshot with normalized multi-horizon performance comparison and quick risk context.

Required outcomes:

- Produce one chart per configured tag/group.
- Each chart has 4 subplots with horizons: `1w`, `4w`, `12w`, `52w`.
- Each subplot uses normalized line series (start at `100`) to compare percent-like relative moves.
- Add a dotted baseline at `100` in every subplot.
- Always show grid on all subplots.
- Legend must be outside the plot area.
- Legend entry format (canonical): `TICKER (1d +1.2%)`.
- Legend change window mapping:
- `1w` subplot legend shows `1d` change.
- `4w` subplot legend shows `1w` change.
- `12w` subplot legend shows `4w` change.
- `52w` subplot legend shows `12w` change.
- Data must be as granular as possible for each horizon; at least one subplot should include >= 200 points.
- Script stdout must print a flat list of all seen tickers with:
- current price
- `1d`, `1w`, `4w`, `12w`, `52w` percentage changes
- annualized volatility
- Tickers to plot come from config in shape: `{ "tag0": ["ticker0", "ticker1"] }`.
- Each tag/group maps to one output plot.
- Document in the skill `SKILL.md` how to change config/groupings to control plotted assets.
- If a `--config` path is passed, it overrides default config path.
- The run should be partial-failure tolerant: skip bad ticker/window data with warnings, and continue plotting/reporting valid data.
- Script stdout contract must be deterministic for automation (no mixed record shapes in CSV stream).

## Solution

- Add a new `meagent-mkt-plot` skill with script-based plotting workflow.
- Default config location should follow repo convention:
- `~/.botbot/meagent-mkt-plot.json`
- Config file defines tag-to-tickers mapping.
- Implement data fetch using a source that supports mixed symbols (indices/ETF/crypto/futures/rates) and historical bars.
- Use partial-failure tolerant fetch semantics:
- if one ticker or one window fails, skip it and continue.
- only fail the run when no ticker has valid daily data.
- For each tag:
- fetch required history once per ticker (enough for 52w panel with fine granularity)
- compute window returns and annualized vol
- include `pct_52w` in computed and printed metrics schema
- build 4 normalized subplots (`1w`, `4w`, `12w`, `52w`)
- place legend outside axes and include mapped change window text
- emit a tabular/flat stdout summary for all unique tickers using one stable CSV schema.
- send non-tabular progress/event lines to stderr so stdout stays machine-parseable.
- Add usage + config examples in `SKILL.md` man-page format.
- Align legend format wording consistently across FD, code, and `SKILL.md`.
- Include sample grouping presets in docs (benchmarks, sectors, crypto, macro).
- Implementation stack (initial):
- `python3` for script runtime
- stdlib: `argparse`, `json`, `pathlib`, `math`, `sys`
- `yfinance` for market data retrieval across mixed tickers
- `matplotlib` for 4-panel plotting and legend/layout control
- `pandas` time-series objects (via `yfinance`) for return/normalization computations

## Files to Modify

- `meagent-mkt-plot/SKILL.md` (new: skill docs with config control instructions and examples)
- `meagent-mkt-plot/*` (new: plotting script and supporting files)
- `~/.botbot/meagent-mkt-plot.json` (runtime config created/read by script; user-local path)

## Verification

- Run skill using default config path and confirm chart(s) render/save per tag.
- Run skill with explicit `--config` and confirm it overrides default path.
- Validate legend formatting and mapping window logic on each subplot.
- Validate all subplots include grid and dotted `100` baseline.
- Confirm normalization starts exactly at `100` for every ticker in every panel.
- Confirm at least one panel has >= 200 plotted points.
- Verify stdout includes each ticker once with price, all requested returns, and annualized vol.
- Verify stdout includes `pct_52w` in header and rows.
- Verify stdout remains machine-parseable CSV (no non-CSV event lines mixed in).
- Verify warnings are emitted for skipped ticker/window data, and run still succeeds when at least one ticker is valid.
- Verify run exits non-zero only when zero valid tickers are available.
- Verify each output tag reports at least one plotted line, or is explicitly marked as no-data in a detectable way.
- Smoke test sample groups:
- Benchmarks: `^GSPC`, `^IXIC`, `^VIX`
- Sectors: `XLK`, `XLF`, `XLE`
- Crypto: `BTC-USD`, `ETH-USD`, `SOL-USD`
- Macro: `^TNX`, `DX-Y.NYB`, `GC=F`

### Verification Plan (Approved 2026-03-11)

1. Run with explicit config override using mixed valid tickers and confirm:
   - one PNG per tag is written
   - each chart has 4 panels (`1w`,`4w`,`12w`,`52w`)
   - grids + dotted `100` baseline + outside legends are present
2. Validate normalization and legend mapping by chart inspection:
   - lines start at `100`
   - legend label pattern is `TICKER (<window> +/-x.x%)`
   - window mapping matches (`1w->1d`, `4w->1w`, `12w->4w`, `52w->12w`)
3. Validate stdout contract:
   - stdout is CSV-only
   - header is exactly `ticker,price,pct_1d,pct_1w,pct_4w,pct_12w,pct_52w,vol_ann`
   - each ticker appears once with stable row shape
4. Validate partial-failure tolerance with mixed valid + invalid ticker.
5. Validate hard failure when all tickers are invalid.
6. Validate default config path behavior without `--config`.

### Verification Results (Executed 2026-03-11)

- Step 1: PASS
  - Command: `uv run --with=yfinance --with=matplotlib meagent-mkt-plot/scripts/meagent_mkt_plot.py run --config /tmp/fd002_valid.json --output-dir /tmp/fd002_out_valid`
  - Outputs: `benchmarks.png`, `crypto.png`
- Step 2: PASS
  - Visual check on `/tmp/fd002_out_valid/benchmarks.png` confirmed visible dotted `100` baseline, grid, legends outside axes, normalized series starting at `100`, and legend window mapping per panel.
- Step 3: PASS
  - Stdout header matched exactly.
  - CSV rows were uniform and ticker-unique.
  - `pct_52w` present in header and rows.
- Step 4: PASS
  - Command with mixed config (`^GSPC` + invalid symbol) exited `0`.
  - Warnings/errors for bad ticker emitted to stderr.
  - Valid ticker row still emitted in stdout CSV.
- Step 5: PASS
  - All-invalid config exited non-zero (`2`).
  - Error message: `no valid ticker daily data fetched; aborting`.
- Step 6: PASS
  - Run without `--config` succeeded using `~/.botbot/meagent-mkt-plot.json`.
  - Produced `defaulttest.png` and valid CSV rows.

## Related

- Request captured from user prompt on 2026-03-10.
- Project convention: runtime config defaults under `~/.botbot/<skill-name>.json`.
