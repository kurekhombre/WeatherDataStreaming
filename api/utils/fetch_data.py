import os

from dotenv import load_dotenv
import aiohttp

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.weatherapi.com/v1"

async def fetch_current_data(city):
    url = f"{BASE_URL}/current.json?key={WEATHER_API_KEY}&q={city}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                print("Data fetched successfully!")
                return data
            else:
                print("Failed to fetch data! Response code: {response.status}")
                return None