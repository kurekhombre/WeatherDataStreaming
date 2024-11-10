from .base_strategy import WeatherStrategy

class CurrentWeatherStrategy(WeatherStrategy):
    def process_dataframe(self, df):
        print("Processing current weather data:")
        print(df.head())