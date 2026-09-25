from __future__ import annotations

import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable, Mapping


TIMEFRAME_MINUTES = {"M5": 5, "M15": 15, "H1": 60, "H4": 240, "D1": 1440}


def rows_to_csv(rows: Iterable[Mapping[str, object]], symbol: str, timeframe: str, output: Path) -> int:
    """Write closed MT5 bars in the Paper Assistant's point-in-time CSV contract."""
    if timeframe not in TIMEFRAME_MINUTES:
        raise ValueError(f"Unsupported timeframe: {timeframe}")
    output.parent.mkdir(parents=True, exist_ok=True)
    minutes = TIMEFRAME_MINUTES[timeframe]
    count = 0
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "event_time_utc", "available_at_utc", "open", "high", "low", "close",
            "spread_points", "tick_volume", "symbol", "source",
        ])
        writer.writeheader()
        for row in rows:
            start = datetime.fromtimestamp(int(row["time"]), tz=timezone.utc)
            close_time = start + timedelta(minutes=minutes)
            writer.writerow({
                "event_time_utc": close_time.isoformat().replace("+00:00", "Z"),
                "available_at_utc": close_time.isoformat().replace("+00:00", "Z"),
                "open": row["open"], "high": row["high"], "low": row["low"], "close": row["close"],
                "spread_points": row["spread"], "tick_volume": row["tick_volume"],
                "symbol": symbol, "source": "MT5",
            })
            count += 1
    return count


def export_closed_bars(symbol: str, timeframe: str, bars: int, output: Path) -> int:
    """Read closed bars only from a locally running MT5 terminal; never sends orders."""
    if bars < 2:
        raise ValueError("bars must be at least 2")
    if timeframe not in TIMEFRAME_MINUTES:
        raise ValueError(f"Unsupported timeframe: {timeframe}")
    import MetaTrader5 as mt5

    mt5_timeframe = getattr(mt5, f"TIMEFRAME_{timeframe}")
    if not mt5.initialize():
        raise RuntimeError(f"MT5 initialize failed: {mt5.last_error()}")
    try:
        if not mt5.symbol_select(symbol, True):
            raise RuntimeError(f"MT5 symbol_select failed for {symbol}: {mt5.last_error()}")
        # Position 1 deliberately skips the still-forming bar, preventing bar-close look-ahead.
        rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 1, bars)
        if rates is None or len(rates) == 0:
            raise RuntimeError(f"MT5 returned no rates for {symbol}: {mt5.last_error()}")
        return rows_to_csv(rates, symbol, timeframe, output)
    finally:
        mt5.shutdown()
