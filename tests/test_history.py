import json
import os
import pytest
from datetime import datetime, timedelta

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import history


def test_save_and_load_snapshot(tmp_path):
    path = str(tmp_path / "history.json")
    snapshot = {"2026-04-27": {"CC": 45, "EC": 12}, "2026-04-28": {"CC": 0, "EC": 3}}
    ts = "2026-04-24T07:02"
    history.save_snapshot(path, ts, snapshot)

    loaded = history.load_history(path)
    assert ts in loaded
    assert loaded[ts] == snapshot


def test_get_previous_snapshot_returns_last_entry(tmp_path):
    path = str(tmp_path / "history.json")
    snap1 = {"2026-04-27": {"CC": 50, "EC": 15}}
    snap2 = {"2026-04-27": {"CC": 45, "EC": 12}}

    history.save_snapshot(path, "2026-04-24T07:00", snap1)
    history.save_snapshot(path, "2026-04-24T13:00", snap2)

    prev = history.get_previous_snapshot(path)
    assert prev == snap2  # most recent = current run's "previous"


def test_get_previous_snapshot_returns_none_when_empty(tmp_path):
    path = str(tmp_path / "history.json")
    result = history.get_previous_snapshot(path)
    assert result is None


def test_prune_removes_entries_older_than_30_days(tmp_path):
    path = str(tmp_path / "history.json")
    old_ts = (datetime.now() - timedelta(days=31)).strftime("%Y-%m-%dT%H:%M")
    recent_ts = datetime.now().strftime("%Y-%m-%dT%H:%M")
    snap = {"2026-04-27": {"CC": 10, "EC": 5}}

    history.save_snapshot(path, old_ts, snap)
    history.save_snapshot(path, recent_ts, snap)
    history.prune_old_entries(path, days=30)

    loaded = history.load_history(path)
    assert old_ts not in loaded
    assert recent_ts in loaded
