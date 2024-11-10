from .base_observer import WeatherObserver

class ConsoleWeatherObserver(WeatherObserver):
    def update(self, data):
        print("New weather data received:", data)