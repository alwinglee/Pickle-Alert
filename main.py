from weatherapi import WeatherAPI
from location import Location
from daylight import Daylight
from rain import Rain
from wind import Wind
from report import Report
from temperature import Temperature

# Number of forecast days (Max 3 due to API free tier limits)
FORECAST_DAYS = 3
# First hour to include in analysis (24-hour format, inclusive). For single-digit hours, omit the leading zero.
# Example: Use 9 for 9 AM, Use 0 for 12 AM, Use 23 for 11 PM
START_TIME = 6
# Last hour to include in analysis (24-hour format, inclusive). For single-digit hours, omit the leading zero.
# Example: Use 9 for 9 AM, Use 0 for 12 AM, Use 23 for 11 PM
END_TIME = 18
# Number of hours displayed in the timeline. Cannot exceed the time range duration specified above.
TOP_TIMELINE_COUNT = 13
# Specifies how many hours before the start time to check for rain (used in Rain class)
RAIN_CHECK_HOURS_PRIOR= 3

def main():
    """
    Validates constant variable values before passing them as arguments, then coordinates fetching weather data,
    parsing it, and printing a report.

    :return: None
    """
    try:
        if not (0 <= START_TIME < 24) or not (0 <= END_TIME < 24):
            raise Exception ("FORMAT ERROR: Invalid time format. Please enter the hour in 24-hour format (0-23)"
                             "as a whole number, without symbols.")

        if END_TIME <=START_TIME:
            raise Exception("END TIME MUST BE AFTER START TIME")

        total_hours = END_TIME-START_TIME+1

        if (total_hours <TOP_TIMELINE_COUNT):
            raise Exception(f"Max. count exceeds time range (set to ≤ {total_hours} hours).")

        if (RAIN_CHECK_HOURS_PRIOR>START_TIME or START_TIME - RAIN_CHECK_HOURS_PRIOR<0):
            raise Exception(f"The rain check period must be within the same day and must not exceed the start time.")

        weather_data= WeatherAPI.fetch_weather_forecast(FORECAST_DAYS)
        location_details = Location(weather_data)
        daylight_details = Daylight(weather_data)
        rain_details = Rain(weather_data, START_TIME, END_TIME, TOP_TIMELINE_COUNT, RAIN_CHECK_HOURS_PRIOR)
        wind_details = Wind(weather_data, START_TIME, END_TIME, TOP_TIMELINE_COUNT)
        temperature_details = Temperature(weather_data, START_TIME, END_TIME, TOP_TIMELINE_COUNT)
        Report(location_details, daylight_details, rain_details, wind_details, temperature_details, START_TIME, END_TIME, total_hours)

    except TypeError:
        print(f"Report Generation Failed:\n"
              f"\t - Integer Input Required")
    except Exception as error:
        print(f"- - - Report Generation Failed - - -\n "
              f"{error}")
main()



