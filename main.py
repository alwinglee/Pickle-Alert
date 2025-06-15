from dotenv import load_dotenv
from weatherapi import WeatherAPI
from location import Location
from daylight import Daylight
from rain import Rain
from wind import Wind

# Number of days to forecast
FORECAST_DAYS = 3

# TODO: Update DocString
def formatReport(locationDetails,daylightDetails,rainDetails,windDetails):
    """
    Takes the string representation of each class and formats it into a customized report.

    :param locationDetails: Customized string from the Location class containing information about the location.
    :param daylightDetails: Customized string from the Daylight class containing information about sunrise and sunset.

    :return: None
    """
    print(f"{locationDetails}\n"
          f"{daylightDetails}\n"
          f"\n- - - SUMMARY - - -\n"
          f"RAIN:\n"
          f"- {rainDetails.rainSummary()}\n"
          f"WIND SPEED:\n"
          f"- {windDetails.windSpeedSummary()}\n"
          f"WIND GUST:\n"
          f"{windDetails}")




def main():
    """
    Coordinates fetching weather data, parsing it, and printing a report.

    :return: None
    """
    weatherData = WeatherAPI.fetchWeatherForecast(FORECAST_DAYS)
    locationDetails = Location(weatherData)
    daylightDetails = Daylight(weatherData)
    rainDetails = Rain(weatherData)
    windDetails = Wind(weatherData)
    formatReport(locationDetails,daylightDetails,rainDetails,windDetails)

main()



