from weatherapi import WeatherAPI
from location import Location
from daylight import Daylight
from rain import Rain
from wind import Wind
from report import Report
from temperature import Temperature
from condition import Condition
from date import Date
from alert import Alert
# from sms import Sms

# Number of forecast days (Max 3 due to API free tier limits)
FORECAST_DAYS = 3
# First hour to include in analysis (24- hour format).For single-digit hours, omit the leading zero
# Use 9 for 9 AM, 22 for 10 PM, and 24 for midnight (current day, not next day)
# Example: 16-20 includes hours 16, 17, 18, and 19 (excludes 20)
START_TIME = 16
# Last hour to include in analysis (24- hour format).For single-digit hours, omit the leading zero
# Use 9 for 9 AM, 22 for 10 PM, and 24 for midnight (current day, not next day)
# Example: 16-20 includes hours 16, 17, 18, and 19 (excludes 20)
END_TIME = 24
# Number of hours displayed in the timeline. Cannot exceed the time range duration specified above.
TOP_TIMELINE_COUNT = 8
# Specifies how many hours before the start time to check for rain (used in Rain class)
RAIN_CHECK_HOURS_PRIOR = 4
# Show Up To Which Days. (E.g. 1 = current day, 2= current day + Next day, 3 = current day + next two days)
DAYS_TO_SHOW = 1

def main():
    """
    Validates constant variable values before passing them as arguments, then coordinates fetching weather data,
    parsing it, and printing a report.

    :return: None
    """
    try:
        if not (0 <= START_TIME <= 23) or not (1 <= END_TIME <= 24):
            raise Exception("Invalid time format. Hours must be START_TIME (0-23) and END_TIME (1-23).")
        if END_TIME <=START_TIME:
            raise Exception("END TIME MUST BE AFTER START TIME")
        total_hours = END_TIME-START_TIME
        if (total_hours <TOP_TIMELINE_COUNT):
            raise Exception(f"Max. count exceeds time range (set to ≤ {total_hours} hours).")
        if (RAIN_CHECK_HOURS_PRIOR>START_TIME or START_TIME - RAIN_CHECK_HOURS_PRIOR<0):
            raise Exception(f"The rain check period must be within the same day and must not exceed the start time.")

        weather_data= WeatherAPI.fetch_weather_forecast(FORECAST_DAYS)
        for each_day in range(DAYS_TO_SHOW):
            location_details = Location(weather_data)
            date_details = Date(weather_data,START_TIME,END_TIME,total_hours, each_day)
            daylight_details = Daylight(weather_data, each_day)
            condition_details = Condition(weather_data, START_TIME, END_TIME, TOP_TIMELINE_COUNT, each_day)
            rain_details = Rain(weather_data, START_TIME, END_TIME, TOP_TIMELINE_COUNT, RAIN_CHECK_HOURS_PRIOR,total_hours, each_day)
            wind_details = Wind(weather_data, START_TIME, END_TIME, TOP_TIMELINE_COUNT,each_day)
            temperature_details = Temperature(weather_data, START_TIME, END_TIME, TOP_TIMELINE_COUNT,each_day)
            report_details = Report(location_details, daylight_details, rain_details, wind_details, temperature_details, condition_details, date_details,  START_TIME, END_TIME, total_hours)
            # Sms(report_details,date_details)
    except TypeError:
        print(f"Report Generation Failed:\n"
              f"\t -  Invalid time format. Please enter the hour in 24-hour format (0-24) as a whole number, without symbols")
    except Exception as error:
        print(f"- - - Report Generation Failed - - -\n "
              f"{error}")
main()



