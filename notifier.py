import requests
import json
import os
import logging

logger = logging.getLogger(__name__)

class DiscordNotifier:
    """Sends notifications to a Discord Webhook."""
    
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_notification(self, job):
        """Sends a job alert to Discord."""
        if not self.webhook_url:
            logger.warning("Discord Webhook URL not configured. Skipping notification.")
            return

        payload = {
            "username": "Job Monitor Bot",
            "embeds": [{
                "title": f"🚀 New Job: {job['title']}",
                "description": f"**Company:** {job['company']}",
                "url": job['link'],
                "color": 5814783, # Nice blue color
                "footer": {
                    "text": "Job Posting Monitor Alert"
                }
            }]
        }

        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"Notification sent for job: {job['id']}")
        except requests.RequestException as e:
            logger.error(f"Failed to send Discord notification: {e}")

class ConsoleNotifier:
    """Fallback notifier that just prints to console."""
    def send_notification(self, job):
        print(f"\n[NEW JOB ALERT]\nTitle: {job['title']}\nCompany: {job['company']}\nLink: {job['link']}\n")
