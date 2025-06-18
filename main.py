from weatherapi import WeatherAPI
from location import Location
from daylight import Daylight
from rain import Rain
from wind import Wind
from report import Report

# Number of forecast days (Max 3 due to API free tier limits)
FORECAST_DAYS = 3
# First hour to include in analysis (24-hour format, inclusive)
START_TIME= 9
# Last hour to include in analysis (24-hour format, inclusive)
END_TIME=22
# Number of hours displayed in the timeline
TOP_TIMELINE_COUNT=5

def main():
    """ 
    Validates constant variable values before passing them as arguments, then coordinates fetching weather data,
    parsing it, and printing a report.

    :return: None
    """
    try:
        if ((0< START_TIME> 24) or (0 <END_TIME>24)):
            raise Exception ("Time not recognized. Please use military (24-hour) format.")
        total_hours = END_TIME-START_TIME
        if (total_hours <=0):
            raise Exception ("End Time Must Be After Start Time")
        if (total_hours <TOP_TIMELINE_COUNT):
            raise Exception(f"Max. count exceeds time range (set to ≤ {total_hours} hours).")
    except TypeError:
        print(f"Report Generation Failed:\n"
              f"\t - Integer Input Required")
    except Exception as e:
        print(f"Report Generation Failed:\n "
              f"\t- {e}\n"
              f"Issue Must Be Resolved Internally Before Proceeding")
    else:
        weatherData = WeatherAPI.fetchWeatherForecast(FORECAST_DAYS)
        locationDetails = Location(weatherData)
        daylightDetails = Daylight(weatherData)
        rainDetails = Rain(weatherData)
        windDetails = Wind(weatherData,START_TIME,END_TIME,TOP_TIMELINE_COUNT)
        Report.formatReport(locationDetails, daylightDetails, rainDetails, windDetails,START_TIME,END_TIME)

main()



