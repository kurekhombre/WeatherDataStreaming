from .base_strategy import WeatherStrategy

class HistoryWeatherStrategy(WeatherStrategy):
    def process_dataframe(self, df):
        print("Processing historical weather data:")
        print(df.head())