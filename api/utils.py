import os
import csv
from datetime import date, timedelta

from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_API_URL = "https://api.weatherapi.com/v1"


def load_cities(filepath="api/cities.csv"):
    cities = []
    with open(filepath, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            cities.append({"name": row["name"], "lat": float(row["lat"]), "lon": float(row["lon"])})
        return cities


def get_api_url(endpoint, lat, lon, days_before=7, days_after=7,):
    if endpoint == "history":
        today = date.today()
        start_dt = (today - timedelta(days=days_before)).strftime("%Y-%m-%d")
        end_dt = today.strftime("%Y-%m-%d")
        return f'{BASE_API_URL}/history.json?q=Warsaw&dt={start_dt}&end_dt={end_dt}&key={WEATHER_API_KEY}'
    elif endpoint == "current":
        return f'{BASE_API_URL}/current.json?q={lat},{lon}&key={WEATHER_API_KEY}'
    elif endpoint == 'forecast':
        return f'{BASE_API_URL}/forecast.json?q={lat},{lon}&days={days_after}&alerts=yes&key={WEATHER_API_KEY}'
    else:
        raise ValueError("Wrong endpoint (available: history, current, forecast) or wrong parameter!")
