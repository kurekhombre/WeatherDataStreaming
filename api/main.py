import asyncio
from utils.fetch_data import fetch_current_data

async def main():
    city = "Warsaw"
    data = await fetch_current_data(city)
    print(data)

if __name__ == "__main__":
    asyncio.run(main())