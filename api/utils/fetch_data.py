import os

import aiohttp
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.weatherapi.com/v1/current.json"

async def fetch_weather_data(city):
    url = f"{BASE_URL}?key={WEATHER_API_KEY}&q={city}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if validate_data_integrity(data):
                    return data
                else:
                    raise ValueError("Data integrity check failed")
            elif response.status == 429:
                raise Exception("API rate limit exceeded")
            elif response.status == 503:
                raise Exception("API is currently unavailable")
            else:
                raise Exception(f"Failed to fetch data. Status code: {response.status}")

def validate_data_integrity(data):
    return "location" in data and "current" in data