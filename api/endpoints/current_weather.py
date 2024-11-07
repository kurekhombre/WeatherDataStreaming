import aiohttp
import asyncio
from api.utils import load_cities, get_api_url

async def fetch_current_weather(session, city):
    url = get_api_url("current", city['lat'], city['lon'])
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            print(f"Weather for {city['name']}: {data} \n")
            return data
        else:
            print(f"Failed to fetch data for {city['name']} \n")
            return None

async def fetch_all_current_weather():
    cities = load_cities()  
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_current_weather(session, city) for city in cities]
        return await asyncio.gather(*tasks)

if __name__ == "__main__":
