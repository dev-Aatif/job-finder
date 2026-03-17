import requests
import logging
from abc import ABC, abstractmethod
from config import REMOTE_OK_URL, USER_AGENT

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Abstract base class for all scrapers."""
    
    @abstractmethod
    def fetch_jobs(self):
        """Fetches jobs and returns a list of dictionaries."""
        pass

class RemoteOKScraper(BaseScraper):
    """
    Scraper for RemoteOK job listings.
    Uses the JSON API to fetch the latest opportunities.
    """
    URL = REMOTE_OK_URL
    HEADERS = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }

    def fetch_jobs(self):
        """Fetches the latest jobs from RemoteOK via JSON API."""
        try:
            logger.info(f"Fetching jobs from {self.URL}")
            response = requests.get(self.URL, headers=self.HEADERS, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            if not isinstance(data, list) or len(data) <= 1:
                logger.warning("No jobs found or invalid API response format.")
                return []

            jobs = []
            # Skip the first item (legal notice)
            for item in data[1:]:
                try:
                    # Basic validation and safe extraction
                    job_id = item.get('id')
                    if not job_id:
                        continue
                        
                    jobs.append({
                        "id": str(job_id),
                        "title": item.get('position', 'No Title'),
                        "company": item.get('company', 'Unknown Company'),
                        "link": item.get('url', '')
                    })
                except Exception as e:
                    logger.debug(f"Error parsing job item: {e}")
                    continue
            
            logger.info(f"Successfully found {len(jobs)} jobs.")
            return jobs
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch jobs: {e}")
            return []
        except ValueError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return []
