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

    def __str__(self):
        """
        Overrides the default '__str__' method to return sunrise/sunset in another format.

        :return: A formatted string displaying sunrise and sunset times on separate lines.
        """
        return (f"Sunrise: {self.sunrise}\n"
                f"Sunset: {self.sunset}")

