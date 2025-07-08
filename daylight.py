from datetime import datetime
class Daylight:
    """
    Represents sunrise and sunset times for a location
    """
    def __init__(self,weather_data):
        """
        Initializes Daylight with sunrise/sunset times extracted from weather API response.

        :param weather_data: Weather forecast response in JSON format.

        :return: None
        """
        self.sunrise = weather_data["forecast"]["forecastday"][0]["astro"]["sunrise"]
        self.sunset = weather_data["forecast"]["forecastday"][0]["astro"]["sunset"]

    def convert_to_military_time(self,time):
        """
        Converts standard time from API data to military time (24-hour format) for sunrise or sunset.

        :param time: Sunrise or sunset time in standard 12-hour format.

        :return: Sunrise or sunset time in military (24-hour) format.
        """
        return datetime.strptime(time,"%I:%M %p").strftime("%H:%M")

    def __str__(self):
        """
        Overrides the default '__str__' method to return sunrise/sunset in another format.

        :return: A formatted string displaying sunrise and sunset times on separate lines.
        """
        return (f"Sunrise: {self.convert_to_military_time(self.sunrise)}\n"
                f"Sunset: {self.convert_to_military_time(self.sunset)}")

