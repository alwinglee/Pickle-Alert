from datetime import datetime
class Date:
    """
    Represents a specific date and time for weather forecast data
    """
    def __init__(self,start_time,end_time,forecast_data):
        """
        Initializes a Date object representing a specific hourly forecast timeframe

        :param start_time: Start time of the hourly timeframe
        :param end_time: End time of the hourly timeframe
        :param forecast_data: Weather forecast data in JSON format

        """
        self.start_time = start_time
        self.end_time = end_time
        self.forecast_data = forecast_data

    def display_forecast_date(self):
        """
        Formats and returns the forecast date from the stored weather data

        :return: Formatted string representation of the forecast date
        """
        return f"{self.forecast_data["date"]}"

    def display_report_date(self):
        """
        Creates a timestamp indicating when this weather forecast report was generated

        :return: Formatted string with the current date and time
        """
        return f"Generated {datetime.now().strftime("%Y-%m-%d | %H:%M %Z")}"

    def display_timeframe(self):
        """
        Formats the start time, end time, and total duration for display

        :return: Formatted string showing the time range and duration
        """
        return (f"Hours: {self.start_time}:00 - {self.end_time}:00 ({self.end_time-self.start_time}h)")

