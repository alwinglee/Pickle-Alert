from datetime import datetime
import os
from twilio.rest import Client
class Report:
    """
    Gathers reports from other metric classes into the main Report class, preparing the data for full report generation
    """
    def __init__(self,location_details, daylight_details, rain_details, wind_details, temperature_details,condition_details,START_TIME,END_TIME,total_hours):
        self.location_details= location_details
        self.daylight_details = daylight_details
        self.rain_details=rain_details
        self.wind_details = wind_details
        self.temperature_details = temperature_details
        self.condition_details=condition_details
        self.START_TIME = self.convert_to_datetime(START_TIME)
        self.END_TIME = self.convert_to_datetime(END_TIME)
        self.total_hours = total_hours
        self.format_report()

    def convert_to_datetime(self,time):
        """
        Converts an integer time value (START_TIME or END_TIME) to a datetime object.

        :param time: An integer representing either the start time or end time in hours (24-hour format)

        :return: A datetime object formatted to display military time (hours and minutes)
        """
        if time==24:
            return datetime.strptime(f"23:59","%H:%M").strftime("%H:%M")
        return datetime.strptime(f"{time:02d}","%H").strftime("%H:%M")

    def format_report(self):
        """
        Takes the string representation of each class and formats it into a customized report

        :return: None
        """
        print (f"{self.location_details}\n"
              f"{self.daylight_details}\n"
              f"\n- - - SUMMARY - - -\n"
              f"Coverage: {self.START_TIME} - {self.END_TIME} ({self.total_hours} hours)\n"
              f"{self.condition_details.condition_summary()}"
              f"{self.rain_details.rain_summary()}"
              f"{self.wind_details.wind_summary()}"
              f"{self.temperature_details.temperature_summary()}"
              f"{self.rain_details.compile_pre_window_rain_report()}"
              f"{self.rain_details.compile_during_window_rain_report()}"
              f"{self.wind_details.compile_wind_report()}"
              f"{self.temperature_details.compile_temperature_report()}")
