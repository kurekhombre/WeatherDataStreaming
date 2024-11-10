import threading

from weather_consumer import WeatherConsumer
from strategies.current_strategy import CurrentWeatherStrategy
from strategies.forecast_strategy import ForecastWeatherStrategy
from strategies.history_strategy import HistoryWeatherStrategy
from observers.console_observer import ConsoleWeatherObserver

if __name__ == "__main__":
    observer = ConsoleWeatherObserver()

    current_consumer = WeatherConsumer(topic="current_weather", group_id="current-group", strategy=CurrentWeatherStrategy())
    current_consumer.add_observer(observer)

    forecast_consumer = WeatherConsumer(topic="forecast_weather", group_id="forecast-group", strategy=ForecastWeatherStrategy())
    forecast_consumer.add_observer(observer)

    history_consumer = WeatherConsumer(topic="history_weather", group_id="history-group", strategy=HistoryWeatherStrategy())
    history_consumer.add_observer(observer)

    threading.Thread(target=current_consumer.consume_and_process).start()
    threading.Thread(target=forecast_consumer.consume_and_process).start()
    threading.Thread(target=history_consumer.consume_and_process).start()
