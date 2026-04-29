# Vande Bharat Monitor

Monitors seat availability for **Vande Bharat Express 20633** (Calicut → Kottayam) via the IRCTC API. Runs on a cron schedule, sends a daily seat-count report by email, and fires urgent alerts via Telegram and Gmail whenever seats drop below a configured threshold or fall sharply between runs.

See [docs/architecture.md](docs/architecture.md) for the system architecture diagram.
