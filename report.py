class Report:
    """"
    A class that formats custom string builders from all classes and generates a structured report.
    """
    def formatReport(locationDetails, daylightDetails, rainDetails, windDetails):
        """
        Takes the string representation of each class and formats it into a customized report.

        :param locationDetails: A custom string from the Location class containing location information.
        :param daylightDetails: A custom string from the Daylight class containing sunrise and sunset times.
        :param rainDetails: A custom string from the Rain class indicating the times of day it will rain and the rainfall
         amount in millimeters.
        :param windDetails: A custom string from the Wind class containing the hours of the highest wind speed and
        wind gust.

        :return: None
        """
        print(f"{locationDetails}\n"
              f"{daylightDetails}\n"
              f"\n- - - SUMMARY - - -\n"
              f"RAIN:\n"
              f"- {rainDetails.rainSummary()}\n"
              f"WIND SPEED:\n"
              f"- {windDetails.windSpeedSummary()}\n"
              f"WIND GUST:\n"
              f"{windDetails}")