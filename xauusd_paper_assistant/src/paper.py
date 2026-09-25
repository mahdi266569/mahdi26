from __future__ import annotations

from dataclasses import dataclass

from .models import Bar, SignalIntent


@dataclass
class Position:
    signal: SignalIntent
    volume: float
    filled_entry: float
    commission: float


def fill(signal: SignalIntent, volume: float, config: dict) -> Position:
    costs = (config["spread_points"] / 2 + config["slippage_points"]) * config["tick_size"]
    entry = signal.entry + costs if signal.side == "BUY" else signal.entry - costs
    return Position(signal, volume, entry, volume * config["commission_per_lot"])


def evaluate(position: Position, bar: Bar, config: dict) -> tuple[str, float] | None:
    """Worst-case policy: when both exit levels occur in one OHLC bar, stop wins."""
    stop_hit = bar.low <= position.signal.stop_loss if position.signal.side == "BUY" else bar.high >= position.signal.stop_loss
    target_hit = bar.high >= position.signal.take_profit if position.signal.side == "BUY" else bar.low <= position.signal.take_profit
    if not stop_hit and not target_hit:
        return None
    exit_price = position.signal.stop_loss if stop_hit else position.signal.take_profit
    direction = 1 if position.signal.side == "BUY" else -1
    ticks = (exit_price - position.filled_entry) * direction / config["tick_size"]
    pnl = ticks * config["tick_value_per_lot"] * position.volume - position.commission
    return ("STOP" if stop_hit else "TARGET", pnl)
