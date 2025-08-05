from datetime import datetime
class Daylight:
    """
    Represents sunrise and sunset times for a location
    """
    def __init__(self,weather_data, forecast_day):
        """
        Initializes Daylight with sunrise/sunset times extracted from weather API response.

        :param weather_data: Weather forecast response in JSON format.

        :return: None
        """
        self.forecast_day = forecast_day
        self.weather_data=weather_data

    def convert_to_military_time(self,time):
        """
        Converts standard time from API data to military time (24-hour format) for sunrise or sunset.

        :param time: Sunrise or sunset time in standard 12-hour format.

        :return: Sunrise or sunset time in military (24-hour) format.
        """
        return datetime.strptime(time,"%I:%M %p").strftime("%H:%M")

    def retrieve_twilight_time(self,days,metric):
        return self.weather_data["forecast"]["forecastday"][days]["astro"][metric]


    def __str__(self):
        """
        Overrides the default '__str__' method to return sunrise/sunset in another format.

        :return: A formatted string displaying sunrise and sunset times on separate lines.
        """
        return (f"\nSunrise: {self.convert_to_military_time(self.retrieve_twilight_time(self.forecast_day,"sunrise"))}\n"
                f"Sunset: {self.convert_to_military_time(self.retrieve_twilight_time(self.forecast_day,"sunset"))}")

