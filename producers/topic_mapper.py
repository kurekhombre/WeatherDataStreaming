KAFKA_TOPICS = {
    "current": "current_weather",
    "forecast": "forecast_weather",
    "history": "history_weather"
}


def get_kafka_topic(data_type):
    return KAFKA_TOPICS.get(data_type)