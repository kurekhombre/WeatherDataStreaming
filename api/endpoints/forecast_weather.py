import aiohttp
import asyncio
from api.utils import load_cities, get_api_url

async def fetch_forecast_weather(session, city):
    url = get_api_url("forecast", city['lat'], city['lon'])
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            print(f"Forecast weather for {city['name']}: {data} \n")
            return data
        else:
            print(f"Failed to fetch forecast data for {city['name']} \n")
            return None

async def fetch_all_forecast_weather():
    cities = load_cities()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_forecast_weather(session, city) for city in cities]
        return await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(fetch_all_forecast_weather())