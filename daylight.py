from datetime import datetime
class Daylight:
    """
    Represents sunrise and sunset times for a location
    """
    def __init__(self,forecast_data):
        self.forecast_data = forecast_data

    def convert_to_military_time(self,time):
        """
        Converts standard time from API data to military time (24-hour format) for sunrise or sunset

        :param time: Sunrise or sunset time in standard 12-hour format

        :return: Sunrise or sunset time in military (24-hour) format
        """
        return datetime.strptime(time,"%I:%M %p").strftime("%H:%M")

    def retrieve_twilight_time(self,metric):
        """
        Retrieves the sunset or sunrise time

        :param metric: Holds either key word 'sunrise' or 'sunset'

        :return: String time of the sunset or sunrise time for the forecasted day
        """
        return self.forecast_data["astro"][metric]

    def __str__(self):
        """
        Overrides the default '__str__' method to return sunrise/sunset in another format.

        :return: A formatted string displaying sunrise and sunset times on separate lines.
        """
        return (f"\nSunrise: {self.convert_to_military_time(self.retrieve_twilight_time("sunrise"))}\n"
                f"Sunset: {self.convert_to_military_time(self.retrieve_twilight_time("sunset"))}")

