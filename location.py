
class Location:
    """
    Represents the geographical location (city, region, country) and local time for specific coordinates.
    """
    def __init__(self,weatherData):
        """
        Initializes Location with geographic details and local time extracted from weather API response.

        :param weatherData: Weather forecast response in JSON format.

        :return: None
        """
        self.weatherData=weatherData
        self.city = self.weatherData["location"]["name"]
        self.region = self.weatherData["location"]["region"]
        self.country=self.weatherData["location"]["country"]
        self.currentDate = self.weatherData["location"]["localtime"]

    def __str__(self):
        """
        Overrides the default '__str__' method to format location details and local time.

        :return: A formatted string with city, region, and country comma-separated on one line,
        and local time on a new line.
        """
        return (f"{self.city}, {self.region}, {self.country}\n"
                f"{self.currentDate}")


