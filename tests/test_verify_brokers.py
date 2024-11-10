import pytest
from unittest.mock import patch, MagicMock
from producers.verify_brokers import verify_brokers

@pytest.mark.parametrize("brokers_available", [True, False])
def test_verify_brokers(brokers_available):
    with patch("producers.verify_brokers.AdminClient") as MockAdminClient:
        mock_client = MockAdminClient.return_value
        mock_metadata = MagicMock()
        mock_metadata.brokers = {1: MagicMock(host="broker-1")} if brokers_available else {}
        mock_client.list_topics.return_value = mock_metadata
        
        result = verify_brokers()
        
        if brokers_available:
            assert result is True
        else:
            assert result is False