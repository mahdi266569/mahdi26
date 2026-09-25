from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analysis import signal_for_closed_bar
from .audit import AuditLog
from .data import load_csv
from .paper import Position, evaluate, fill
from .risk import decide


def run(data_path: Path, config_path: Path, audit_dir: Path) -> dict:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    bars, issues = load_csv(data_path)
    audit = AuditLog(audit_dir, config)
    for issue in issues:
        audit.write("DATA_QUALITY_REJECT", reason=issue)
    equity = daily_start_equity = config["initial_equity"]
    position: Position | None = None
    trades = wins = 0
    for index, bar in enumerate(bars):
        if position:
            result = evaluate(position, bar, config)
            if result:
                outcome, pnl = result
                equity += pnl
                trades += 1
                wins += outcome == "TARGET"
                audit.write("TRADE_CLOSED", event_time_utc=bar.event_time, outcome=outcome, pnl=round(pnl, 4), equity=round(equity, 4))
                position = None
        signal = signal_for_closed_bar(bars[: index + 1], config)
        if not signal:
            continue
        decision = decide(signal, equity, daily_start_equity, int(position is not None), config)
        audit.write("RISK_DECISION", event_time_utc=bar.event_time, strategy_version=config["strategy_version"], approved=decision.approved, reason_codes=decision.reason_codes, volume=decision.volume)
        if decision.approved and position is None:
            position = fill(signal, decision.volume, config)
            audit.write("PAPER_FILL", event_time_utc=bar.event_time, side=signal.side, entry=position.filled_entry, stop_loss=signal.stop_loss, take_profit=signal.take_profit, volume=decision.volume, reason=signal.reason)
    summary = {"mode": "PAPER", "bars": len(bars), "data_issues": len(issues), "closed_trades": trades, "wins": wins, "equity": round(equity, 4), "open_position": position is not None}
    (audit_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic paper-only XAUUSD research runner")
    sub = parser.add_subparsers(dest="command", required=True)
    backtest = sub.add_parser("backtest")
    backtest.add_argument("--data", type=Path, required=True)
    backtest.add_argument("--config", type=Path, required=True)
    backtest.add_argument("--audit-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "backtest":
        print(json.dumps(run(args.data, args.config, args.audit_dir), indent=2))


if __name__ == "__main__":
    main()
