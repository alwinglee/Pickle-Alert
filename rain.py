from io import StringIO
from datetime import datetime
class Rain:
    """
    A class to filter, analyze, and report rain-related weather data.
    """
    def __init__(self,weather_data):
        """
        Initializes the Rain class with key rain-related metrics from an API response and sets evaluation thresholds
        for rain impact levels.

        :param weather_data: Weather forecast response in JSON format.

        :return: None
        """
        self.weather_data=weather_data
        self.string_builder = StringIO()
        self.will_it_rain = self.weather_data["forecast"]["forecastday"][0]["day"]["daily_will_it_rain"]
        self.chance_of_rain = self.weather_data["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"]
        self.total_precipitation = self.weather_data["forecast"]["forecastday"][0]["day"]["totalprecip_mm"]
        self.rain_description = self.weather_data["forecast"]["forecastday"][0]["day"]["condition"]["text"]
        self.RAIN_CHANCE_LOW_THRESH=30
        self.RAIN_CHANCE_HIGH_THRESH = 70
        self.RAIN_PRECIPITATION_LOW_THRESH=2.5
        self.RAIN_PRECIPITATION_HIGH_THRESH=7.5

    def rain_summary(self):
        """
        Generates a summary of the rain condition for the day, including impact assessments.

        :return: String containing the day's rain status, including impact level description when applicable.
        """
        if (self.will_it_rain ==0):
            return (f"Will It Rain: NO")
        else:
            self.rain_timeline()
            return(f"Will It Rain: YES ({self.rain_description})\n"
                  f"Chance of Rain:{self.chance_of_rain_impact()}IMPACT ({self.chance_of_rain}%) \n"
                  f"Total Precipitation: {self.total_precipitation_impact()} IMPACT ({self.total_precipitation}mm)")

    def chance_of_rain_impact(self):
        """
        Classifies rain probability into one of three impact levels.

        :return: String containing the impact level and description.
        """
        if (self.chance_of_rain <self.RAIN_CHANCE_LOW_THRESH):
            return ("MINIMAL (BRIEF)")
        elif (self.chance_of_rain <self.RAIN_CHANCE_HIGH_THRESH ):
            return ("MODERATE (SCATTERED)")
        else:
            return ("MAXIMUM (PERSISTENT)")

    def total_precipitation_impact(self):
        """
        Determines rain precipitation into one of three impact levels.

        :return: String containing the impact level and description.
        """
        if (self.total_precipitation<self.RAIN_PRECIPITATION_LOW_THRESH):
            return ("MINIMAL (NO ACCUMULATION)")
        elif (self.total_precipitation<self.RAIN_PRECIPITATION_HIGH_THRESH):
            return ("MODERATE (PUDDLES)")
        else:
            return ("MAXIMUM (FLOODING)")

    def rain_timeline(self):
        """
        Generates hourly rain forecast data formatted as a chronological timeline.

        Each entry includes:
            - Time (HH:MM format)
            - Chance of rain (percentage)
            - Expected precipitation amount (mm)

        return: None
        """
        self.string_builder.write("- - - RAIN REPORT - - -")
        currentDay = self.weather_data["forecast"]["forecastday"][0]["hour"]
        times = [
            {   "time":datetime.strptime(each_hour["time"],("%Y-%m-%d %H:%M")).strftime("%H:%M"),"chance_of_rain":each_hour["chance_of_rain"],
                "precipitation": each_hour["precip_mm"] }for each_hour in currentDay if each_hour["will_it_rain"] !=0
            ]
        sortByChanceOfRain = sorted(times,key=lambda item:item["chance_of_rain"],reverse=True)

        for each_sortedTimes in sortByChanceOfRain:
            self.string_builder.write(f"{each_sortedTimes["time"]}: {each_sortedTimes["chance_of_rain"]}({each_sortedTimes["precipitation"]})")

    def __str__(self):
        """
        Overrides the default '__str__' method to return rain forecast data in another format.

        :return: A formatted string displaying rain impact levels and forecasted rain times on separate lines.
        """
        return self.string_builder.getvalue()





