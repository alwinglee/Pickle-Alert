
from weatherapi import WeatherAPI
from location import Location
from daylight import Daylight
from rain import Rain
from wind import Wind
from report import Report

# Number of days to forecast
FORECAST_DAYS = 3


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
    Report.formatReport(locationDetails,daylightDetails,rainDetails,windDetails)
main()



