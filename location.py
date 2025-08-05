from datetime import datetime
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
        self.weather_data = weather_data

    def retrieve_location_details(self, metric):
        return self.weather_data["location"][metric]

    def __str__(self):
        """
        Overrides the default '__str__' method to format location details and local time.

        :return: A formatted string with city, region, and country comma-separated on one line,
        and local time on a new line.
        """
        return (f"= = = LOCATION = = =\n"
                f"{self.retrieve_location_details("name")}, {self.retrieve_location_details("region")}, "
                f"{self.retrieve_location_details("country")}")



