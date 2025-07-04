from datetime import datetime
class Report:
    """
    Gathers reports from other metric classes into the main Report class, preparing the data for full report generation
    """
    def __init__(self,location_details, daylight_details, rain_details, wind_details, temperature_details,START_TIME,END_TIME,total_hours):
        self.location_details= location_details
        self.daylight_details = daylight_details
        self.rain_details=rain_details
        self.wind_details = wind_details
        self.temperature_details = temperature_details
        self.START_TIME = datetime.strptime(f"{START_TIME:02d}", "%H").strftime("%H:%M")
        self.END_TIME = datetime.strptime(f"{END_TIME:02d}", "%H").strftime("%H:%M")
        self.total_hours = total_hours
        self.format_report()

    def format_report(self):
        """
        Takes the string representation of each class and formats it into a customized report

        :return: None
        """
        print(f"{self.location_details}\n"
              f"{self.daylight_details}\n"
              f"\n- - - SUMMARY - - -\n"
              f"ANALYSIS PERIOD:\n"
              f"{self.START_TIME} - {self.END_TIME} ({self.total_hours} hours)\n"
              f"{self.rain_details.compile_pre_window_rain_report()}"
              f"{self.rain_details.compile_during_window_rain_report()}"
              f"{self.wind_details.compile_wind_report()}"
              f"{self.temperature_details.compile_temperature_report()}")
