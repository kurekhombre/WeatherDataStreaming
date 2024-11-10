import pytest
from unittest.mock import patch, MagicMock
from producers.check_ssl_connection import check_ssl_connection

def test_ssl_connection_success():
    with patch("producers.check_ssl_connection.Producer") as MockProducer:
        mock_producer_instance = MockProducer.return_value
        mock_producer_instance.produce.return_value = None
        mock_producer_instance.flush.return_value = None
        
        result = check_ssl_connection()
        
        assert result is True
        print("Test passed: SSL connection established successfully.")

def test_ssl_connection_failure():
    with patch("producers.check_ssl_connection.Producer") as MockProducer:
        MockProducer.side_effect = Exception("SSL connection failed.")
        
        result = check_ssl_connection()
        
        assert result is False
        print("Test passed: SSL connection failed as expected.")
