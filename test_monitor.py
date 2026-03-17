import json
import os
import unittest
from unittest.mock import MagicMock, patch
from monitor import run_monitor
from config import DB_FILE
from scraper import RemoteOKScraper
from notifier import DiscordNotifier

class TestJobMonitor(unittest.TestCase):
    def setUp(self):
        # Clear database before each test
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)

    def tearDown(self):
        # Clean up database after each test
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)

    @patch('monitor.RemoteOKScraper.fetch_jobs')
    @patch('monitor.DiscordNotifier.send_notification')
    def test_new_job_detection(self, mock_notify, mock_fetch):
        # Mock initial fetch
        mock_fetch.return_value = [
            {"id": "1", "title": "Job 1", "company": "Co 1", "link": "http://1"},
            {"id": "2", "title": "Job 2", "company": "Co 2", "link": "http://2"}
        ]
        
        # Run monitor first time
        run_monitor()
        
        # Check if notifications were sent
        self.assertEqual(mock_notify.call_count, 2)
        
        # Check if database was created
        self.assertTrue(os.path.exists(DB_FILE))
        with open(DB_FILE, 'r') as f:
            data = json.load(f)
            self.assertIn("1", data["seen_ids"])
            self.assertIn("2", data["seen_ids"])

        # Reset mock and run again with one new job
        mock_notify.reset_mock()
        mock_fetch.return_value.append({"id": "3", "title": "Job 3", "company": "Co 3", "link": "http://3"})
        
        run_monitor()
        
        # Should only notify for the NEW job
        self.assertEqual(mock_notify.call_count, 1)
        mock_notify.assert_called_with({"id": "3", "title": "Job 3", "company": "Co 3", "link": "http://3"})

if __name__ == "__main__":
    unittest.main()
