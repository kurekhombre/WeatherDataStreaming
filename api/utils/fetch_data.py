import os

from dotenv import load_dotenv
import aiohttp

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.weatherapi.com/v1"

async def fetch_current_data(city):
    url = f"{BASE_URL}/current.json?key={WEATHER_API_KEY}&q={city}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if validate_data_integrity(data):
                        print("Data fetched successfully!")
                        return data
                    else:
                        raise ValueError("Data integrity check failed.")
                elif response.status == 429:
                    print("Rate limit exceeded.")
                    raise Exception("API rate limit exceeded.")
                elif response.status == 503:
                    print("API is currently unavailable.")
                    raise Exception("API is currently unavailable.")
                else:
                    print(f"Failed to fetch data. Status code: {response.status}")
                    raise Exception(f"Failed to fetch data with status {response.status}")
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    
def validate_data_integrity(data):
    return "location" in data and "current" in data