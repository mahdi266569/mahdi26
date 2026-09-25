from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Bar:
    event_time: datetime
    available_at: datetime
    open: float
    high: float
    low: float
    close: float
    spread_points: float
    tick_volume: float
    symbol: str
    source: str


@dataclass(frozen=True)
class SignalIntent:
    side: str
    entry: float
    stop_loss: float
    take_profit: float
    event_time: datetime
    reason: str


@dataclass(frozen=True)
class RiskDecision:
    approved: bool
    reason_codes: tuple[str, ...]
    volume: float
    risk_amount: float
