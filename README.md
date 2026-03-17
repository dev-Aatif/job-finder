# Job Posting Monitor 🤖

A robust Python-based automation tool that monitors job sites, detects new listings, and sends notifications via Discord/Slack webhooks.

## Features
- **Site Monitoring**: Currently configured for RemoteOK using a modular scraper interface.
- **Keyword Filtering**: Optionally filter jobs based on specific keywords (e.g., "Python", "Remote").
- **State Management**: Uses a simple JSON database to avoid duplicate notifications.
- **Notifications**: Supports Discord webhooks and console logging.
- **Containerized**: Ready for deployment with Docker.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Copy `.env.example` to `.env` and configure your settings:
   ```bash
   cp .env.example .env
   ```
   *Edit `.env` to include your Discord URL and optional keywords.*

3. **Run Locally**:
   ```bash
   python monitor.py
   ```

## Development & Deployment

### Running with Docker
```bash
docker build -t job-monitor .
docker run --env-file .env job-monitor
```

### Automation (Cron Job)
To run every hour:
```bash
0 * * * * /usr/bin/python3 /path/to/automation/monitor.py >> /path/to/automation/monitor.log 2>&1
```

## Project Structure
- `monitor.py`: Main entry point and orchestration logic.
- `scraper.py`: Modular scraper implementations (uses `BaseScraper`).
- `notifier.py`: Notification delivery handlers.
- `config.py`: Centralized configuration and environment loading.
- `logger_config.py`: Centralized logging setup.
- `database.json`: Local persistence for seen job IDs.
- `requirements.txt`: Pinned dependency list.
- `Dockerfile`: Deployment container configuration.
```
