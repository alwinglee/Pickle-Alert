from datetime import datetime
import os
from twilio.rest import Client
class Report:
    """
    Gathers reports from other metric classes into the main Report class, preparing the data for full report generation
    """
    def __init__(self, location_details, daylight_details, rain_details, wind_details, temperature_details,
                 condition_details, date_details, alert_details):
        self.location_details = location_details
        self.daylight_details = daylight_details
        self.rain_details = rain_details
        self.wind_details = wind_details
        self.temperature_details = temperature_details
        self.condition_details = condition_details
        self.date_details = date_details
        self.alert_details = alert_details
        self.formatted_report = self.format_report()

    def format_report(self):
        """
        Takes the string representation of each class and formats it into a customized report

        :return: A string containing the structured report
        """
        return (f"[{self.date_details.display_forecast_date()}]\n"
                f"[{self.date_details.display_generation_date()}]\n"
                f"\n= = = 🗺️ LOCATION 🗺️ = = =\n"
                f"{self.location_details}"
                f"{self.daylight_details}\n"
                f"\n= = = 📝 SUMMARY 📝 = = =\n"
                f"{self.date_details.display_timeframe_summary()}\n"
                f"{self.condition_details.condition_summary()}"
                f"{self.alert_details.alert_summary()}"
                f"{self.rain_details.rain_summary()}"
                f"{self.wind_details.wind_summary()}"
                f"{self.temperature_details.temperature_summary()}"
                f"{self.alert_details.alert_report()}"
                f"{self.rain_details.compile_pre_window_rain_report()}"
                f"{self.rain_details.compile_during_window_rain_report()}"
                f"{self.wind_details.compile_wind_report()}"
                f"{self.temperature_details.compile_temperature_report()}\n")