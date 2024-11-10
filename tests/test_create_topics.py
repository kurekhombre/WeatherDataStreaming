import pytest
from unittest.mock import patch, MagicMock
from producers.create_topics import create_topics

def test_create_topics():
    with patch("producers.create_topics.AdminClient") as MockAdminClient:
        mock_admin_instance = MockAdminClient.return_value
        mock_admin_instance.create_topics.return_value = {
            "current_weather": MagicMock(),
            "forecast_weather": MagicMock(),
            "history_weather": MagicMock(),
        }
        
        for topic, future in mock_admin_instance.create_topics.return_value.items():
            future.result.return_value = None

        create_topics()
        print("Test passed: Topics created successfully.")
