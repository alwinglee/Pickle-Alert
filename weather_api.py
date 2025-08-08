import requests
import os
from dotenv import load_dotenv

class WeatherAPI:
    """
    A class to interact with a weather API and fetch forecast data.
    """
    def fetch_weather_forecast(MAX_FORECAST_DAYS):
        """
        Sends a request to the API server with specific parameters to retrieve the weather forecast for the current day
        and the next two days.

        :param MAX_FORECAST_DAYS: Number of days to include in forecast

        :return: The API's weather forecast response in JSON format.
        """
        try:
            load_dotenv()
            weather_response = requests.get(os.getenv("URL"), params={"q": f"{os.getenv("LAT")},{os.getenv("LON")}",
                                                                      "key": os.getenv("API_KEY"), "days": MAX_FORECAST_DAYS})
            weather_response.raise_for_status()
            weather_response_json= weather_response.json()
        except requests.exceptions.ConnectionError:
            raise Exception(f"NETWORK ERROR: FAILED TO CONNECT TO SERVER")
        except requests.exceptions.HTTPError:
            raise Exception(f"REQUEST ERROR: SERVER REJECTED REQUEST ({weather_response.status_code} error)")
        except requests.exceptions.JSONDecodeError:
            raise Exception(f"JSON ERROR: INVALID JSON RETURNED")
        except requests.exceptions.RequestException as error:
            raise Exception(f"MISCELLANEOUS ERROR: {error}")
        else:
            return weather_response_json


