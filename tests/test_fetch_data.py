import pytest
import asyncio
from api.utils.fetch_data import fetch_current_data

@pytest.mark.asyncio
async def test_fetch_weather_data():
    city = "Warsaw"
    data = await fetch_current_data(city)
    assert data is not None, "Data shouldn't be None"
    assert "location" in data, "Response should contain location data"
    assert "current" in data, "Response should contain current weather data"