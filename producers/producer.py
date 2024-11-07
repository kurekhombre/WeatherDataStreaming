import json
import asyncio

from api.endpoints.history_weather import fetch_all_history_weather
from api.endpoints.current_weather import fetch_all_current_weather
from api.endpoints.forecast_weather import fetch_all_forecast_weather

from producers.topic_mapper import get_kafka_topic

from confluent_kafka import Producer


def create_kafka_producer():
    producer_config = {
        'bootstrap.servers': 'localhost:9092'
    }
    return Producer(producer_config)

def send_to_kafka(producer, topic, message):
    producer.produce(topic, json.dumps(message).encode('utf-8'))
    producer.flush()

async def produce_history_weather(producer):
    data = await fetch_all_history_weather()
    topic = get_kafka_topic("history")
    for item in data:
        if item is not None:
            send_to_kafka(producer, topic, item)

async def produce_current_weather(producer):
    data = await fetch_all_current_weather()
    topic = get_kafka_topic("current")
    for item in data:
        if item is not None:
            send_to_kafka(producer, topic, item)

async def produce_forecast_weather(producer):
    data = await fetch_all_forecast_weather()
    topic = get_kafka_topic("forecast")
    for item in data:
        if item is not None:
            send_to_kafka(producer, topic, item)

async def main():
    producer = create_kafka_producer()
    while True:
        print("Producing current weather data...")
        await produce_current_weather(producer)

        print("Producing forecast weather data...")
        await produce_forecast_weather(producer)

        print("Producing historical weather data...")
        await produce_history_weather(producer)

        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())