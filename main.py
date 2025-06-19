from weatherapi import WeatherAPI
from location import Location
from daylight import Daylight
from rain import Rain
from wind import Wind
from report import Report

# Number of forecast days (Max 3 due to API free tier limits)
FORECAST_DAYS = 3
# First hour to include in analysis (24-hour format, inclusive). For single-digit hours, omit the leading zero.
# Example: Use '9' for 9 AM
START_TIME= 9
# Last hour to include in analysis (24-hour format, inclusive). For single-digit hours, omit the leading zero.
# Example: Use '9' for 9 AM
END_TIME=10
# Number of hours displayed in the timeline. Cannot exceed the time range duration specified above.
TOP_TIMELINE_COUNT=1

def main():
    """ 
    Validates constant variable values before passing them as arguments, then coordinates fetching weather data,
    parsing it, and printing a report.

    :return: None
    """
    try:
        if ((0< START_TIME> 24) or (0 <END_TIME>24)):
            raise Exception ("Invalid time format. Please enter the hour in 24-hour format (0-23) "
                             "as a whole number, without symbols.")
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
        weather_data = WeatherAPI.fetchWeatherForecast(FORECAST_DAYS)
        location_details = Location(weather_data)
        daylight_details = Daylight(weather_data)
        rain_details = Rain(weather_data)
        wind_details = Wind(weather_data,START_TIME,END_TIME,TOP_TIMELINE_COUNT)
        Report.format_report(location_details, daylight_details, rain_details, wind_details,START_TIME,END_TIME)
main()



