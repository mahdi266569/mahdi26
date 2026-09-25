from __future__ import annotations

import math

from .models import RiskDecision, SignalIntent


def decide(signal: SignalIntent, equity: float, daily_start_equity: float, open_positions: int, config: dict) -> RiskDecision:
    reasons: list[str] = []
    if equity <= 0 or daily_start_equity <= 0:
        reasons.append("INVALID_EQUITY")
    if open_positions >= config["max_open_positions"]:
        reasons.append("MAX_OPEN_POSITIONS")
    if (daily_start_equity - equity) / daily_start_equity * 100 >= config["max_daily_drawdown_pct"]:
        reasons.append("DAILY_CIRCUIT_BREAKER")
    distance = abs(signal.entry - signal.stop_loss)
    if distance <= 0:
        reasons.append("INVALID_STOP_DISTANCE")
    rr = abs(signal.take_profit - signal.entry) / distance if distance else 0
    if rr < config["min_rr"]:
        reasons.append("RR_BELOW_MINIMUM")
    ticks = distance / config["tick_size"] if config["tick_size"] > 0 else 0
    loss_per_lot = ticks * config["tick_value_per_lot"]
    risk_amount = equity * config["max_risk_pct"] / 100
    if loss_per_lot <= 0:
        reasons.append("INVALID_TICK_PARAMETERS")
        return RiskDecision(False, tuple(reasons), 0.0, risk_amount)
    raw_volume = risk_amount / loss_per_lot
    step = config["volume_step"]
    volume = math.floor(raw_volume / step) * step
    volume = round(volume, 8)
    if volume < config["volume_min"]:
        reasons.append("MIN_VOLUME_EXCEEDS_RISK")
    if volume > config["volume_max"]:
        volume = config["volume_max"]
    return RiskDecision(not reasons, tuple(reasons), volume if not reasons else 0.0, risk_amount)
