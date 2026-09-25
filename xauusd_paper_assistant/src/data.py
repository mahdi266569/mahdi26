from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from .models import Bar

REQUIRED_COLUMNS = {
    "event_time_utc", "available_at_utc", "open", "high", "low", "close",
    "spread_points", "tick_volume", "symbol", "source",
}


def _time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_csv(path: Path) -> tuple[list[Bar], list[str]]:
    """Load only bars that were available at their stated decision time."""
    bars: list[Bar] = []
    issues: list[str] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not REQUIRED_COLUMNS.issubset(reader.fieldnames):
            missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            raise ValueError(f"CSV missing required columns: {sorted(missing)}")
        previous_time: datetime | None = None
        for index, row in enumerate(reader, start=2):
            try:
                bar = Bar(
                    event_time=_time(row["event_time_utc"]), available_at=_time(row["available_at_utc"]),
                    open=float(row["open"]), high=float(row["high"]), low=float(row["low"]),
                    close=float(row["close"]), spread_points=float(row["spread_points"]),
                    tick_volume=float(row["tick_volume"]), symbol=row["symbol"], source=row["source"],
                )
            except (TypeError, ValueError) as exc:
                issues.append(f"ROW_{index}:PARSE_ERROR:{exc}")
                continue
            if bar.available_at > bar.event_time:
                issues.append(f"ROW_{index}:LOOK_AHEAD_AVAILABLE_AT")
            elif bar.tick_volume <= 0 or bar.low > min(bar.open, bar.close, bar.high) or bar.high < max(bar.open, bar.close, bar.low):
                issues.append(f"ROW_{index}:INVALID_OHLC_OR_VOLUME")
            elif previous_time and bar.event_time <= previous_time:
                issues.append(f"ROW_{index}:NON_MONOTONIC_TIME")
            else:
                bars.append(bar)
                previous_time = bar.event_time
    return bars, issues
