#!/usr/bin/env python3
import argparse
import json
import math
import re
import sys
from pathlib import Path


class CliError(RuntimeError):
    pass


WINDOW_DAYS = {
    "1d": 1,
    "1w": 5,
    "4w": 20,
    "12w": 60,
    "52w": 252,
}


PANELS = [
    {"horizon": "1w", "period": "7d", "interval": "30m", "legend_window": "1d"},
    {"horizon": "4w", "period": "1mo", "interval": "60m", "legend_window": "1w"},
    {"horizon": "12w", "period": "3mo", "interval": "1d", "legend_window": "4w"},
    {"horizon": "52w", "period": "1y", "interval": "1d", "legend_window": "12w"},
]


def warn(message: str) -> None:
    print(f"warn: {message}", file=sys.stderr)


def load_config(path: Path) -> dict[str, list[str]]:
    if not path.exists():
        raise CliError(f"missing config: {path}")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CliError(f"invalid JSON config: {path}: {exc}") from exc
    if not isinstance(raw, dict) or not raw:
        raise CliError("config must be a non-empty JSON object in shape {\"tag\": [\"TICKER\"]}")
    out: dict[str, list[str]] = {}
    for key, value in raw.items():
        tag = str(key or "").strip()
        if not tag:
            raise CliError("config contains a blank tag key")
        if not isinstance(value, list) or not value:
            raise CliError(f"config[{tag!r}] must be a non-empty array of tickers")
        tickers: list[str] = []
        for item in value:
            ticker = str(item or "").strip()
            if not ticker:
                raise CliError(f"config[{tag!r}] contains blank ticker")
            tickers.append(ticker)
        out[tag] = tickers
    return out


def fetch_close_series(ticker: str, period: str, interval: str):
    try:
        import yfinance as yf
    except ModuleNotFoundError as exc:
        raise CliError("missing dependency: yfinance (run with `uv run --with=yfinance ...`)") from exc

    try:
        frame = yf.download(
            ticker,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=True,
            threads=False,
        )
    except Exception as exc:
        warn(f"{ticker}: fetch failed for period={period} interval={interval}: {exc}")
        return None
    if frame is None or frame.empty:
        warn(f"{ticker}: no data for period={period} interval={interval}")
        return None
    if "Close" in frame.columns:
        series = frame["Close"].dropna()
    elif hasattr(frame.columns, "levels") and "Close" in frame.columns.get_level_values(0):
        close_frame = frame.xs("Close", axis=1, level=0)
        if close_frame.empty:
            warn(f"{ticker}: empty Close frame for period={period} interval={interval}")
            return None
        series = close_frame.iloc[:, 0].dropna()
    else:
        warn(f"{ticker}: missing Close column for period={period} interval={interval}")
        return None
    if getattr(series, "ndim", 1) != 1:
        if getattr(series, "shape", (0, 0))[1] < 1:
            warn(f"{ticker}: close series frame has no columns for period={period} interval={interval}")
            return None
        series = series.iloc[:, 0]
    if series.empty:
        warn(f"{ticker}: empty close series for period={period} interval={interval}")
        return None
    try:
        if getattr(series.index, "tz", None) is not None:
            series.index = series.index.tz_convert(None)
    except Exception:
        pass
    series = series[~series.index.duplicated(keep="last")].sort_index()
    if len(series) < 2:
        warn(f"{ticker}: insufficient points for period={period} interval={interval}")
        return None
    return series


def pct_move(series, days: int):
    if len(series) <= days:
        return None
    now = float(series.iloc[-1])
    prev = float(series.iloc[-1 - days])
    if prev == 0:
        return None
    return (now / prev - 1.0) * 100.0


def annualized_volatility(daily_close):
    if len(daily_close) < 2:
        return None
    returns = daily_close.pct_change().dropna()
    if returns.empty:
        return None
    vol = float(returns.std()) * math.sqrt(252.0) * 100.0
    if math.isnan(vol):
        return None
    return vol


def fmt_metric(value):
    if value is None:
        return ""
    return f"{value:.4f}"


def fmt_legend_change(value):
    if value is None:
        return "n/a"
    return f"{value:+.1f}%"


def slugify(tag: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", tag.strip()).strip("-")
    return slug or "untitled"


def write_table_image(rows: list[dict[str, object]], path: Path) -> None:
    try:
        import pandas as pd
    except ModuleNotFoundError as exc:
        raise CliError("missing dependency: pandas (installed with yfinance)") from exc
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:
        raise CliError("missing dependency: matplotlib (run with `uv run --with=matplotlib ...`)") from exc

    ordered = []
    for row in sorted(rows, key=lambda item: (str(item["group"]), str(item["ticker"]))):
        ordered.append(
            {
                "group": row["group"],
                "ticker": row["ticker"],
                "price": fmt_metric(row["price"]),
                "pct_1d": fmt_metric(row["pct_1d"]),
                "pct_1w": fmt_metric(row["pct_1w"]),
                "pct_4w": fmt_metric(row["pct_4w"]),
                "pct_12w": fmt_metric(row["pct_12w"]),
                "pct_52w": fmt_metric(row["pct_52w"]),
                "vol_ann": fmt_metric(row["vol_ann"]),
            }
        )
    frame = pd.DataFrame(
        ordered,
        columns=["group", "ticker", "price", "pct_1d", "pct_1w", "pct_4w", "pct_12w", "pct_52w", "vol_ann"],
    )
    pct_cols = {"pct_1d", "pct_1w", "pct_4w", "pct_12w", "pct_52w"}
    col_idx = {name: idx for idx, name in enumerate(frame.columns)}
    rows_n = max(len(frame), 1)
    fig_h = max(3.0, min(18.0, 1.1 + rows_n * 0.42))
    fig, ax = plt.subplots(figsize=(14, fig_h))
    ax.axis("off")
    tbl = ax.table(
        cellText=frame.values,
        colLabels=frame.columns,
        loc="center",
        cellLoc="left",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1.0, 1.25)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_linewidth(0.25)
        cell.set_edgecolor("#cfd8e3")
        if r == 0:
            cell.set_text_props(weight="bold")
            cell.set_facecolor("#e9eef5")
            continue

        base = "#f7f9fc" if r % 2 == 0 else "#ffffff"
        cell.set_facecolor(base)

        col_name = frame.columns[c]
        if col_name not in pct_cols:
            continue
        text = str(frame.iloc[r - 1, c]).strip()
        if not text:
            continue
        try:
            value = float(text)
        except ValueError:
            continue
        if value > 0:
            cell.set_facecolor("#d9f2e6")
        elif value < 0:
            cell.set_facecolor("#f8dddd")

    if len(frame) > 1:
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        last_col = len(frame.columns) - 1
        inv = ax.transAxes.inverted()
        for i in range(len(frame) - 1):
            if str(frame.iloc[i]["group"]) == str(frame.iloc[i + 1]["group"]):
                continue

            # Header is row 0; data starts at row 1.
            next_row = i + 2
            left_bbox = tbl[(next_row, 0)].get_window_extent(renderer)
            right_bbox = tbl[(next_row, last_col)].get_window_extent(renderer)

            x0, y = inv.transform((left_bbox.x0, left_bbox.y1))
            x1, _ = inv.transform((right_bbox.x1, right_bbox.y1))
            ax.plot([x0, x1], [y, y], transform=ax.transAxes, color="#374151", linewidth=2.8, solid_capstyle="butt")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def run() -> int:
    parser = argparse.ArgumentParser(prog="meagent_mkt_plot.py")
    subparsers = parser.add_subparsers(dest="subcmd", required=True)
    subparsers.add_parser("run", help="generate normalized multi-horizon market plots")
    parser.parse_args(sys.argv[1:])

    cfg_path = Path.home() / ".botbot" / "meagent-mkt-plot.json"
    groups = load_config(cfg_path)

    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:
        raise CliError("missing dependency: matplotlib (run with `uv run --with=matplotlib ...`)") from exc

    output_dir = Path("/tmp")
    output_dir.mkdir(parents=True, exist_ok=True)

    metrics_by_ticker: dict[str, dict[str, object]] = {}
    daily_cache: dict[str, object] = {}
    panel_cache: dict[tuple[str, str], object] = {}
    image_paths: list[Path] = []

    for tickers in groups.values():
        for ticker in tickers:
            if ticker in daily_cache:
                continue
            daily = fetch_close_series(ticker, period="2y", interval="1d")
            daily_cache[ticker] = daily
            if daily is None:
                continue
            metrics_by_ticker[ticker] = {
                "ticker": ticker,
                "price": float(daily.iloc[-1]),
                "pct_1d": pct_move(daily, WINDOW_DAYS["1d"]),
                "pct_1w": pct_move(daily, WINDOW_DAYS["1w"]),
                "pct_4w": pct_move(daily, WINDOW_DAYS["4w"]),
                "pct_12w": pct_move(daily, WINDOW_DAYS["12w"]),
                "pct_52w": pct_move(daily, WINDOW_DAYS["52w"]),
                "vol_ann": annualized_volatility(daily),
            }

    if not metrics_by_ticker:
        raise CliError("no valid ticker daily data fetched; aborting")

    for tag, tickers in groups.items():
        fig, axes = plt.subplots(4, 1, figsize=(14, 16))
        axes_list = list(axes)
        tag_has_any_line = False

        for axis, panel in zip(axes_list, PANELS):
            horizon = panel["horizon"]
            interval = panel["interval"]
            period = panel["period"]
            legend_window = panel["legend_window"]

            axis.set_title(horizon)
            axis.axhline(100.0, linestyle=":", linewidth=1.1, color="gray")
            axis.grid(True, linestyle=":", linewidth=0.8, alpha=0.6)
            axis.tick_params(axis="x", labelrotation=45)

            subplot_has_line = False
            for ticker in tickers:
                if ticker not in metrics_by_ticker:
                    continue
                cache_key = (ticker, horizon)
                if cache_key not in panel_cache:
                    panel_cache[cache_key] = fetch_close_series(ticker, period=period, interval=interval)
                series = panel_cache[cache_key]
                if series is None:
                    continue
                start = float(series.iloc[0])
                if start == 0:
                    warn(f"{ticker}: skipping {horizon} panel because normalized base is zero")
                    continue
                normalized = (series / start) * 100.0
                legend_value = metrics_by_ticker[ticker][f"pct_{legend_window}"]
                axis.plot(
                    normalized.index,
                    normalized.values,
                    linewidth=1.8,
                    label=f"{ticker} {legend_window}:{fmt_legend_change(legend_value)}",
                    drawstyle="steps-post",
                )
                subplot_has_line = True
                tag_has_any_line = True

            if subplot_has_line:
                axis.legend(
                    loc="center left",
                    bbox_to_anchor=(1.0, 0.5),
                    frameon=False,
                    fontsize=7,
                    handlelength=1.0,
                    handletextpad=0.3,
                    labelspacing=0.2,
                    borderaxespad=0.15,
                )
            else:
                axis.text(
                    0.5,
                    0.5,
                    "NO DATA",
                    transform=axis.transAxes,
                    ha="center",
                    va="center",
                    fontsize=12,
                    color="gray",
                )

        fig.suptitle(f"{tag} market comparison", fontsize=15)
        fig.tight_layout(rect=[0, 0, 0.94, 0.98])
        out_file = output_dir / f"{slugify(tag)}.png"
        fig.savefig(out_file, dpi=150)
        image_paths.append(out_file)
        plt.close(fig)

        if tag_has_any_line:
            print(f"info: wrote {out_file}", file=sys.stderr)
        else:
            print(f"warn: wrote {out_file} (no-data)", file=sys.stderr)

    table_rows: list[dict[str, object]] = []
    for tag, tickers in groups.items():
        for ticker in tickers:
            if ticker not in metrics_by_ticker:
                continue
            row = dict(metrics_by_ticker[ticker])
            row["group"] = tag
            table_rows.append(row)

    overview_path = output_dir / "overview.png"
    write_table_image(table_rows, overview_path)
    print(overview_path)
    for path in image_paths:
        print(path)
    return 0


def main() -> int:
    try:
        return run()
    except CliError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("error: interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
