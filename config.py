import os
from dotenv import load_dotenv

load_dotenv()

# Project Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "database.json")

# API Configurations
REMOTE_OK_URL = "https://remoteok.com/api"

# Notifiers
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Filtering (Optional)
# List of keywords to filter jobs (comma-separated in .env)
_keywords = os.getenv("JOB_KEYWORDS", "")
KEYWORDS = [k.strip().lower() for k in _keywords.split(",")] if _keywords else []

# Scraper Settings
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
