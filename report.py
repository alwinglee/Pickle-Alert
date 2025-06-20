class Report:
    """"
    A class that formats custom string builders from all classes and generates a structured report.
    """
    def get_am_or_pm(hour):
        """
        Assigns an 'AM' or 'PM' suffix to the given time passed into the function

        :param hour: An integer representing either the start or end hour of the time range.

        :return:  the time including the appropriate 'AM' or 'PM' designation.
        """
        if (hour <12):
            return f"{hour} AM"
        else:
            return f"{hour} PM"

    def format_report(location_details, daylight_details, rain_details, wind_details, START_TIME, END_TIME):
        """
        Takes the string representation of each class and formats it into a customized report.

        :param location_details: A custom string from the Location class containing location information.
        :param daylight_details: A custom string from the Daylight class containing sunrise and sunset times.
        :param rain_details: A custom string from the Rain class indicating the times of day it will rain and the rainfall
         amount in millimeters.
        :param wind_details: A custom string from the Wind class containing the hours of the highest wind speed and
        wind gust.
        :param START_TIME: A custom string from the Wind class containing the hours of the highest wind speed and
        wind gust.
        :param END_TIME: A custom string from the Wind class containing the hours of the highest wind speed and
        wind gust.

        :return: None
        """
        print(f"{location_details}\n"
              f"{daylight_details}\n"
              f"\n- - - SUMMARY - - -\n"
              f"ANALYSIS PERIOD: {Report.get_am_or_pm(START_TIME)} - {Report.get_am_or_pm(END_TIME)}\n"
              f"RAIN:\n"
              f"- {rain_details.rain_summary()}\n"
              f"WIND SPEED:\n"
              f"- {wind_details.wind_speed_summary()}\n"
              f"WIND GUST:\n"
              f"- {wind_details.wind_gust_summary()}\n"
              f"{wind_details}")