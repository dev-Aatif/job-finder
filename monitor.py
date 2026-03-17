import json
import os
import logging
from logger_config import setup_logging
from config import DB_FILE, DISCORD_WEBHOOK_URL, KEYWORDS
from scraper import RemoteOKScraper
from notifier import DiscordNotifier, ConsoleNotifier

# Initialize logging once
setup_logging()
logger = logging.getLogger(__name__)

def load_seen_jobs():
    """Loads already recorded job IDs from the database."""
    if not os.path.exists(DB_FILE):
        return set()
    try:
        with open(DB_FILE, 'r') as f:
            data = json.load(f)
            return set(data.get("seen_ids", []))
    except (json.JSONDecodeError, Exception) as e:
        logger.error(f"Error loading database: {e}")
        return set()

def save_seen_jobs(seen_ids):
    """Saves job IDs to the database."""
    try:
        with open(DB_FILE, 'w') as f:
            json.dump({"seen_ids": list(seen_ids)}, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving database: {e}")

def matches_keywords(job):
    """Checks if a job title or description matches configured keywords."""
    if not KEYWORDS:
        return True
    
    text = f"{job['title']} {job['company']}".lower()
    return any(keyword in text for keyword in KEYWORDS)

def run_monitor():
    """Main execution loop for checking new jobs."""
    logger.info("Starting Job Monitor check...")
    
    seen_ids = load_seen_jobs()
    scraper = RemoteOKScraper()
    current_jobs = scraper.fetch_jobs()
    
    if not current_jobs:
        logger.warning("No jobs found in this run.")
        return

    # Initialize notifiers
    notifiers = [ConsoleNotifier()]
    if DISCORD_WEBHOOK_URL:
        # Check if URL is valid start
        if DISCORD_WEBHOOK_URL.startswith("http"):
            notifiers.append(DiscordNotifier(DISCORD_WEBHOOK_URL))
    
    new_jobs_found = 0
    
    for job in current_jobs:
        job_id = job['id']
        if job_id not in seen_ids:
            # Apply keyword filtering if configured
            if not matches_keywords(job):
                logger.debug(f"Skipping job {job['title']} (no keyword match)")
                continue

            logger.info(f"New job detected: {job['title']} at {job['company']}")
            for notifier in notifiers:
                notifier.send_notification(job)
            
            seen_ids.add(job_id)
            new_jobs_found += 1

    if new_jobs_found > 0:
        save_seen_jobs(seen_ids)
        logger.info(f"Check complete. Found {new_jobs_found} new jobs.")
    else:
        logger.info("Check complete. No new jobs found.")

if __name__ == "__main__":
    run_monitor()
