import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import alerts


PREV = {
    "2026-04-27": {"CC": 50, "EC": 15},
    "2026-04-28": {"CC": 100, "EC": 40},
}
CURR = {
    "2026-04-27": {"CC": 45, "EC": 3},   # EC dropped 80% and below 10
    "2026-04-28": {"CC": 65, "EC": 28},  # CC dropped 35%
}


def test_detect_low_seats():
    breaches = alerts.detect_breaches(CURR, PREV, min_seats=10, drop_percent=30)
    dates = [b["date"] for b in breaches]
    assert "2026-04-27" in dates  # EC=3 < 10


def test_detect_drop_percent():
    breaches = alerts.detect_breaches(CURR, PREV, min_seats=10, drop_percent=30)
    classes_on_28 = [b["class"] for b in breaches if b["date"] == "2026-04-28"]
    assert "CC" in classes_on_28  # 100→65 = 35% drop


def test_no_breach_when_within_threshold():
    curr = {"2026-04-27": {"CC": 80, "EC": 20}}
    prev = {"2026-04-27": {"CC": 90, "EC": 25}}
    breaches = alerts.detect_breaches(curr, prev, min_seats=10, drop_percent=30)
    assert breaches == []


def test_no_breach_when_no_previous():
    curr = {"2026-04-27": {"CC": 5, "EC": 2}}
    breaches = alerts.detect_breaches(curr, None, min_seats=10, drop_percent=30)
    # No previous → only check min_seats threshold
    dates = [b["date"] for b in breaches]
    assert "2026-04-27" in dates


def test_format_report_contains_all_dates():
    report = alerts.format_report(CURR, label="Morning")
    assert "2026-04-27" in report
    assert "2026-04-28" in report
    assert "Morning" in report


def test_format_alert_message():
    breach = {"date": "2026-04-27", "class": "EC", "prev": 15, "curr": 3, "drop_pct": 80}
    msg = alerts.format_alert_message([breach])
    assert "EC" in msg
    assert "2026-04-27" in msg
    assert "80%" in msg
