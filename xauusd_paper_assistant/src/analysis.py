from __future__ import annotations

from .models import Bar, SignalIntent


def atr(bars: list[Bar], period: int) -> float | None:
    if len(bars) < period + 1:
        return None
    ranges = []
    for index in range(-period, 0):
        current, previous = bars[index], bars[index - 1]
        ranges.append(max(current.high - current.low, abs(current.high - previous.close), abs(current.low - previous.close)))
    return sum(ranges) / period


def signal_for_closed_bar(bars: list[Bar], config: dict) -> SignalIntent | None:
    """Point-in-time BOS + FVG detector. It intentionally has no LLM or OF input."""
    left, right = config["swing_left_bars"], config["swing_right_bars"]
    lookback = left + right + 3
    if len(bars) < max(lookback, config["atr_period"] + 1):
        return None
    current, middle, first = bars[-1], bars[-2], bars[-3]
    current_atr = atr(bars, config["atr_period"])
    if current_atr is None:
        return None
    confirmed = bars[-(right + 1)]
    prior = bars[-(right + left + 1):-(right + 1)]
    swing_high = all(confirmed.high > bar.high for bar in prior)
    swing_low = all(confirmed.low < bar.low for bar in prior)
    min_gap = current_atr * config["fvg_min_gap_atr"]
    if swing_high and current.close > confirmed.high and first.high < current.low and current.low - first.high >= min_gap:
        entry, stop = current.close, min(first.low, middle.low, current.low) - current_atr
        return SignalIntent("BUY", entry, stop, entry + 2 * (entry - stop), current.event_time, "CONFIRMED_BULLISH_BOS_FVG")
    if swing_low and current.close < confirmed.low and first.low > current.high and first.low - current.high >= min_gap:
        entry, stop = current.close, max(first.high, middle.high, current.high) + current_atr
        return SignalIntent("SELL", entry, stop, entry - 2 * (stop - entry), current.event_time, "CONFIRMED_BEARISH_BOS_FVG")
    return None
