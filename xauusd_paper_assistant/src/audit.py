from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AuditLog:
    def __init__(self, directory: Path, config: dict[str, Any]) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        self.path = directory / "events.jsonl"
        self.config_hash = hashlib.sha256(
            json.dumps(config, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()

    def write(self, event_type: str, **fields: Any) -> None:
        event = {
            "logged_at_utc": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "mode": "PAPER",
            "config_hash": self.config_hash,
            **fields,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True, default=str) + "\n")
