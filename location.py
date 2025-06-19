
class Location:
    """
    Represents the geographical location (city, region, country) and local time for specific coordinates.
    """
    def __init__(self,weather_data):
        """
        Initializes Location with geographic details and local time extracted from weather API response.

        :param weather_data: Weather forecast response in JSON format.

        :return: None
        """
        self.weather_data=weather_data
        self.city = self.weather_data["location"]["name"]
        self.region = self.weather_data["location"]["region"]
        self.country=self.weather_data["location"]["country"]
        self.current_data = self.weather_data["location"]["localtime"]

    def __str__(self):
        """
        Overrides the default '__str__' method to format location details and local time.

        :return: A formatted string with city, region, and country comma-separated on one line,
        and local time on a new line.
        """
        return (f"{self.city}, {self.region}, {self.country}\n"
                f"{self.current_data}")


