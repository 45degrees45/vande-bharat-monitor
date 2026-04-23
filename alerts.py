from datetime import datetime


def detect_breaches(
    current: dict,
    previous: dict | None,
    min_seats: int,
    drop_percent: float,
) -> list[dict]:
    """
    Compare current and previous snapshots.
    Returns list of breach dicts: {date, class, prev, curr, drop_pct, reason}.
    reason is 'low' | 'drop' | 'both'
    """
    breaches = []
    for travel_date, classes in current.items():
        for cls, curr_count in classes.items():
            if curr_count == -1:
                continue  # waitlist, skip threshold logic

            prev_count = None
            if previous and travel_date in previous:
                prev_count = previous[travel_date].get(cls)

            reasons = []

            if curr_count < min_seats:
                reasons.append("low")

            if prev_count is not None and prev_count > 0:
                drop_pct = (prev_count - curr_count) / prev_count * 100
                if drop_pct >= drop_percent:
                    reasons.append("drop")
            else:
                drop_pct = 0.0

            if reasons:
                breaches.append({
                    "date": travel_date,
                    "class": cls,
                    "prev": prev_count,
                    "curr": curr_count,
                    "drop_pct": round(drop_pct, 1),
                    "reason": "+".join(reasons),
                })
    return breaches


def _seat_emoji(count: int) -> str:
    if count == -1:
        return "⚠️"
    if count < 10:
        return "🔴"
    return "✅"


def format_report(current: dict, label: str) -> str:
    """Build a human-readable report string for Telegram/Gmail."""
    today = datetime.now().strftime("%b %d")
    lines = [f"🚆 *Vande Bharat 20633 | {label} | {today}*\n"]
    for travel_date in sorted(current.keys()):
        classes = current[travel_date]
        parts = []
        for cls in ["CC", "EC"]:
            count = classes.get(cls, -1)
            emoji = _seat_emoji(count)
            label_str = "WL" if count == -1 else str(count)
            parts.append(f"{cls}={label_str}{emoji}")
        lines.append(f"`{travel_date}` — {' | '.join(parts)}")
    return "\n".join(lines)


def format_alert_message(breaches: list[dict]) -> str:
    """Build an urgent alert message for Telegram."""
    lines = ["🚨 *Vande Bharat ALERT — Book Now!*\n"]
    for b in breaches:
        prev_str = str(b["prev"]) if b["prev"] is not None else "?"
        lines.append(
            f"`{b['date']}` → *{b['class']}*: {prev_str} → {b['curr']} seats "
            f"({b['drop_pct']}% drop)"
        )
    lines.append("\nBook: https://www.confirmtkt.com/train/20633")
    return "\n".join(lines)
