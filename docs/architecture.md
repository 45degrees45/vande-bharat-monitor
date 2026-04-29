# Architecture

Vande Bharat Monitor is a Python cron job that polls the IRCTC seat-availability API for train 20633 (Calicut → Kottayam), compares the current snapshot against the previous run, and sends a daily report via Gmail plus urgent alerts via Telegram and Gmail whenever seats drop below a threshold or fall sharply.

```mermaid
flowchart TD
    CRON[Cron / manual run\nmain.py] --> CFG[config.json\ntrain, stations, thresholds,\nTelegram & Gmail creds]
    CRON --> SCRAPER[scraper.py\ncurl_cffi Chrome-impersonation]

    SCRAPER -->|warm-up GET /nget/| IRCTC[IRCTC avlFarenquiry API\nclasses CC & EC\nup to 5 pagination hops]
    IRCTC -->|seat counts per date| SCRAPER
    SCRAPER -->|snapshot dict| CRON

    CRON --> HISTORY[history.py\ndata/history.json]
    HISTORY -->|previous snapshot| CRON

    CRON --> ALERTS[alerts.py\ndetect_breaches\nformat_report / format_alert_message]
    ALERTS -->|breach list + formatted text| CRON

    CRON -->|daily report email| GMAIL[Gmail SMTP\nsmtp.gmail.com:465]
    CRON -->|breach alert email| GMAIL
    CRON -->|breach alert message| TELEGRAM[Telegram Bot API\napi.telegram.org]

    CRON --> SAVE[history.py\nsave_snapshot + prune_old_entries\ndata/history.json]
    CRON --> LOG[logs/run.log]
```
