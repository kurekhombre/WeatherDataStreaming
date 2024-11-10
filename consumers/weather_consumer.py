from confluent_kafka import Consumer
import pandas as pd
import json
import os

from dotenv import load_dotenv


load_dotenv()

BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER")
KAFKA_CONFLUENCE_API_KEY = os.getenv("KAFKA_CONFLUENCE_API_KEY")
KAFKA_CONFLUENCE_API_SECRET = os.getenv("KAFKA_CONFLUENCE_API_SECRET")

class WeatherConsumer:
    def __init__(self, topic, group_id, strategy):
        self.topic = topic
        self.group_id = group_id
        self.strategy = strategy
        self.consumer = self.create_kafka_consumer()
        self.observers = []

    def create_kafka_consumer(self):
        consumer_config = {
            'bootstrap.servers': BOOTSTRAP_SERVER,
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL',
            'sasl.username': KAFKA_CONFLUENCE_API_KEY,
            'sasl.password': KAFKA_CONFLUENCE_API_SECRET,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest'
        }
        return Consumer(consumer_config)

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, data):
        for observer in self.observers:
            observer.update(data)

    def consume_and_process(self):
        self.consumer.subscribe([self.topic])
        messages = []

        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue

                data = json.loads(msg.value().decode('utf-8'))
                messages.append(data)
                self.notify_observers(data)
                if len(messages) >= 10:
                    df = pd.DataFrame(messages)
                    self.strategy.process_dataframe(df)
                    messages = []

        except KeyboardInterrupt:
            print("Consuming interrupted by user")
        finally:
            self.consumer.close()