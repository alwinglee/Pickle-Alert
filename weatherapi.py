import requests
import os
from dotenv import load_dotenv

class WeatherAPI:
    """
    A class to interact with a weather API and fetch forecast data.
    """
    # TODO: Create Try Except
    def fetchWeatherForecast(FORECAST_DAYS):
        """
        Sends a request to the API server with specific parameters to retrieve the weather forecast for the current day
        and the next two days.

        :param FORECAST_DAYS: Number of days to include in forecast

        :return: The API's weather forecast response in JSON format.
        """
        load_dotenv()
        weatherResponse = requests.get(os.getenv("URL"), params={"q": f"{os.getenv("LAT")},{os.getenv("LON")}",
                                                                 "key": os.getenv("API_KEY"), "days": FORECAST_DAYS})
        return weatherResponse.json()
