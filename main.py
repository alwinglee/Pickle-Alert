import requests
from dotenv import load_dotenv
import os
from location import Location
from daylight import Daylight

# Number of days to forecast
FORECAST_DAYS = 3

# TODO: Create Try Except
def fetchWeatherForecast():
    """
    Sends a request to the API server with specific parameters to retrieve the weather forecast for the current day
    and the next two days.

    :return: The API's weather forecast response in JSON format.
    """
    weatherResponse = requests.get(os.getenv("URL"), params= {"q": f"{os.getenv("LAT")},{os.getenv("LON")}",
                                                              "key": os.getenv("API_KEY"), "days": FORECAST_DAYS})
    return weatherResponse.json()

def formatReport(locationDetails,daylightDetails):
    """
    Takes the string representation of each class and formats it into a customized report.

    :param locationDetails: Customized string from the Location class containing information about the location.
    :param daylightDetails: Customized string from the Daylight class containing information about sunrise and sunset.

    :return: None
    """
    print(f"{locationDetails}\n"
          f"{daylightDetails}")

def main():
    """
    Coordinates fetching weather data, parsing it, and printing a report.

    :return: None
    """
    load_dotenv()
    weatherData = fetchWeatherForecast()
    locationDetails = Location(weatherData)
    daylightDetails = Daylight(weatherData)
    formatReport(locationDetails,daylightDetails)

main()






