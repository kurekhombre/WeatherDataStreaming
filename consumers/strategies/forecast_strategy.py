from .base_strategy import WeatherStrategy

class ForecastWeatherStrategy(WeatherStrategy):
    def process_dataframe(self, df):
        print("Processing forecast weather data:")
        print(df.head())