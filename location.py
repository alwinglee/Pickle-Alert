from datetime import datetime
class Location:
    """
    Represents the geographical location (city, region, country) and local time for specific coordinates
    """
    def __init__(self,forecast_location_data):
        self.forecast_location_data = forecast_location_data

    def retrieve_location_details(self, metric):
        """
        Retrieves the details of the geographical location

        :param metric: Attributes of the geographical location such as 'name', 'region', and 'country'

        :return: String value of the retrieved location attribute
        """
        return self.forecast_location_data[metric]

    def __str__(self):
        """
        Overrides the default '__str__' method to format location details and local time

        :return: A formatted string with city, region, and country
        """
        return (f"{self.retrieve_location_details("name")}, {self.retrieve_location_details("region")}, "
                f"{self.retrieve_location_details("country")}")



