from weather_api import Weather_API
from location import Location
from daylight import Daylight
from rain import Rain
from wind import Wind
from report import Report
from temperature import Temperature
from condition import Condition
from date import Date
from configuration import Configuration
# from sms import Sms

# Show Up To Which Days (E.g. 1 = current day, 2= current day + Next day, 3 = current day + next two days, and etc)
# (Minimum: 1 day | Maximum: 14 days (currently limited to 3 days on free tier))
DAYS_TO_SHOW = 1
# First hour to include in analysis (24- hour format).For single-digit hours, omit the leading zero.
# Use 9 for 9 AM, 22 for 10 PM, and 24 for midnight (current day, not next day)
# Example: 16-20 includes hours 16, 17, 18, and 19 (excludes 20)
START_TIME = 16
# Last hour to include in analysis (24- hour format).For single-digit hours, omit the leading zero
# Use 9 for 9 AM, 22 for 10 PM, and 24 for midnight (current day, not next day)
# Example: 16-20 includes hours 16, 17, 18, and 19 (excludes 20)
END_TIME = 22
# Number of hours displayed in the timeline report. Cannot exceed the time range duration specified above.
TOP_TIMELINE_COUNT = 6
# Specifies how many hours before the start time to check for rain (used in Rain class)
RAIN_CHECK_HOURS_PRIOR = 4

def main():
    """
    Validates constant variable values before passing them as arguments, then coordinates fetching weather data,
    parsing it, and printing a report.

    :return: None
    """
    try:
        Configuration(START_TIME, END_TIME, TOP_TIMELINE_COUNT, RAIN_CHECK_HOURS_PRIOR, DAYS_TO_SHOW)
        duration = END_TIME-START_TIME
        weather_data = Weather_API.fetch_weather_forecast(DAYS_TO_SHOW)
        for forecast_day in range(DAYS_TO_SHOW):
            location_details = Location(weather_data)
            date_details = Date(weather_data,START_TIME,END_TIME, duration, forecast_day)
            daylight_details = Daylight(weather_data,forecast_day)
            condition_details = Condition(weather_data, START_TIME, END_TIME, TOP_TIMELINE_COUNT, forecast_day)
            rain_details = Rain(weather_data, START_TIME, END_TIME, duration, TOP_TIMELINE_COUNT, RAIN_CHECK_HOURS_PRIOR, forecast_day)
            wind_details = Wind(weather_data, START_TIME, END_TIME, TOP_TIMELINE_COUNT,forecast_day)
            temperature_details = Temperature(weather_data, START_TIME, END_TIME, TOP_TIMELINE_COUNT,forecast_day)
            report_details = Report(location_details, daylight_details, rain_details, wind_details, temperature_details, condition_details, date_details,  START_TIME, END_TIME, duration)
            # Sms(report_details,date_details)
    except Exception as error:
        print(f"Report Generation Failed:\n"
              f"{error}")
main()



