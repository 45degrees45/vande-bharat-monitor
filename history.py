import json
import os
from datetime import datetime, timedelta


def load_history(path: str) -> dict:
    """Load full history dict from JSON file. Returns {} if missing or empty."""
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        content = f.read().strip()
    if not content:
        return {}
    return json.loads(content)


def save_snapshot(path: str, timestamp: str, snapshot: dict) -> None:
    """Append a new timestamped snapshot to the history file."""
    data = load_history(path)
    data[timestamp] = snapshot
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def get_previous_snapshot(path: str) -> dict | None:
    """Return the most recent snapshot (last entry by key sort), or None if no history."""
    data = load_history(path)
    if not data:
        return None
    latest_key = sorted(data.keys())[-1]
    return data[latest_key]


def prune_old_entries(path: str, days: int = 30) -> None:
    """Remove entries older than `days` days from the history file."""
    data = load_history(path)
    cutoff = datetime.now() - timedelta(days=days)
    pruned = {
        ts: snap
        for ts, snap in data.items()
        if datetime.fromisoformat(ts) >= cutoff
    }
    with open(path, "w") as f:
        json.dump(pruned, f, indent=2)
