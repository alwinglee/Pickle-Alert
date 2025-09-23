from datetime import datetime
class Date:
    """
    Represents a specific date and time for weather forecast data
    """
    def __init__(self, start_time, end_time, forecast_data):
        self.start_time = self.convert_to_datetime(start_time)
        self.end_time = self.convert_to_datetime(end_time)
        self.forecast_data = forecast_data

    def display_forecast_date(self):
        """
        Formats and returns the forecast date from the stored weather data

        :return: Formatted string representation of the forecast date
        """
        return f"Forecast {self.forecast_data["date"]}"

    def display_generation_date(self):
        """
        Creates a timestamp indicating when this weather forecast report was generated

        :return: Formatted string with the current date and time
        """
        return f"Generated {datetime.now().strftime("%Y-%m-%d | %H:%M%Z")}"

    def display_timeframe_summary(self):
        """
        Formats the start time, end time, and total duration for display

        :return: Formatted string showing the time range and duration
        """
        return f"Hours: {self.start_time}- {self.end_time}"

    def convert_to_datetime(self,time):
        """
        Converts an integer time value (start_time or end_time) to a datetime object.

        :param time: An integer representing either the start time or end time in hours (24-hour format)

        :return: A datetime object formatted to display military time (hours and minutes)
        """
        if time == 24:
            return datetime.strptime(f"23:59", "%H:%M").strftime("%H:%M")
        return datetime.strptime(f"{time:02d}:00", "%H:%M").strftime("%H:%M")
