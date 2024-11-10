import pytest
from unittest.mock import AsyncMock, patch
from api.utils.fetch_data import fetch_weather_data, validate_data_integrity


@pytest.mark.asyncio
async def test_fetch_weather_data_integrity():
    class MockResponse:
        status = 200
        async def json(self):
            return {
                "location": {"name": "Warsaw", "country": "Poland"},
                "current": {"temp_c": 20.0, "condition": {"text": "Sunny"}}
            }
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass

    with patch("aiohttp.ClientSession.get", return_value=MockResponse()):
        data = await fetch_weather_data("Warsaw")
        assert validate_data_integrity(data) is True, "Data should have valid structure"
        assert "location" in data, "Data should contain 'location' key"
        assert "current" in data, "Data should contain 'current' key"


@pytest.mark.asyncio
async def test_fetch_weather_data_rate_limit_handling():
    mock_response = AsyncMock()
    mock_response.status = 429

    with patch("aiohttp.ClientSession.get", return_value=mock_response):
        with pytest.raises(Exception):
            await fetch_weather_data("Warszawa")
        

@pytest.mark.asyncio
async def test_fetch_weather_data_api_downtime():
    mock_response = AsyncMock()
    mock_response.status = 503

    with patch("aiohttp.ClientSession.get", return_value=mock_response):
        with pytest.raises(Exception):
            await fetch_weather_data("Warszawa")


@pytest.mark.asyncio
async def test_fetch_weather_data_invalid_parameters():
    mock_response = AsyncMock()
    mock_response.status = 400
    mock_response.json.return_value = {"error": "Invalid request"}

    with patch("aiohttp.ClientSession.get", return_value=mock_response):
        with pytest.raises(Exception, match="Failed to fetch data"):
            await fetch_weather_data("InvalidCityName")