import aiohttp
import asyncio
from api.utils import load_cities, get_api_url

async def fetch_history_weather(session, city, days_before=7):
    url = get_api_url("history", city['lat'], city['lon'], days_before=days_before)
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            print(f"Historical weather for {city['name']}: {data} \n")
            return data
        else:
            print(f"Failed to fetch historical weather for {city['name']} \n")
            return None

async def fetch_all_history_weather(days_before=7):
    cities = load_cities()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_history_weather(session, city, days_before=days_before) for city in cities]
        return await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(fetch_all_history_weather())