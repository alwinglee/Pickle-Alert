from io import StringIO
from datetime import datetime
class Rain:
    """
    A class to filter, analyze, and report rain-related weather data.
    """
    def __init__(self,weatherData):
        """
        Initializes the Rain class with key rain-related metrics from an API response and sets evaluation thresholds
        for rain impact levels.

        :param weatherData: Weather forecast response in JSON format.

        :return: None
        """
        self.weatherData=weatherData
        self.stringBuilder = StringIO()
        self.willItRain = self.weatherData["forecast"]["forecastday"][0]["day"]["daily_will_it_rain"]
        self.chanceOfRain = self.weatherData["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"]
        self.totalPrecipitation = self.weatherData["forecast"]["forecastday"][0]["day"]["totalprecip_mm"]
        self.rainDescription = self.weatherData["forecast"]["forecastday"][0]["day"]["condition"]["text"]
        self.RAIN_CHANCE_LOW_THRESH=30
        self.RAIN_CHANCE_HIGH_THRESH = 70
        self.RAIN_PRECIPITATION_LOW_THRESH=2.5
        self.RAIN_PRECIPITATION_HIGH_THRESH=7.5

    def rainSummary(self):
        """
        Generates a summary of the rain condition for the day, including impact assessments.

        :return: String containing the day's rain status, including impact level description when applicable.
        """
        if (self.willItRain ==0):
            return ("Will It Rain: NO")
        else:
            self.rainTimeline()
            return(f"Will It Rain: YES ({self.rainDescription})\n"
                  f"Chance of Rain:{self.chanceOfRainImpact()}IMPACT ({self.chanceOfRain}%) \n"
                  f"Total Precipitation: {self.totalPrecipitationImpact()} IMPACT ({self.totalPrecipitation}mm)")

    def chanceOfRainImpact(self):
        """
        Classifies rain probability into one of three impact levels.

        :return: String containing the impact level and description.
        """
        if (self.chanceOfRain <self.RAIN_CHANCE_LOW_THRESH):
            return ("MINIMAL (BRIEF)")
        elif (self.chanceOfRain <self.RAIN_CHANCE_HIGH_THRESH ):
            return ("MODERATE (SCATTERED)")
        else:
            return ("MAXIMUM (PERSISTENT)")

    def totalPrecipitationImpact(self):
        """
        Determines rain precipitation into one of three impact levels.

        :return: String containing the impact level and description.
        """
        if (self.totalPrecipitation<self.RAIN_PRECIPITATION_LOW_THRESH):
            return ("MINIMAL (NO ACCUMULATION)")
        elif (self.totalPrecipitation<self.RAIN_PRECIPITATION_HIGH_THRESH):
            return ("MODERATE (PUDDLES)")
        else:
            return ("MAXIMUM (FLOODING)")

    def rainTimeline(self):
        """
        Generates hourly rain forecast data formatted as a chronological timeline.

        Each entry includes:
            - Time (HH:MM format)
            - Chance of rain (percentage)
            - Expected precipitation amount (mm)

        return: None
        """
        self.stringBuilder.write("- - - RAIN REPORT - - -")
        currentDay = self.weatherData["forecast"]["forecastday"][0]["hour"]
        times = [
            {   "time":datetime.strptime(each_hour["time"],("%Y-%m-%d %H:%M")).strftime("%H:%M"),"chanceOfRain":each_hour["chance_of_rain"],
                "precipitation": each_hour["precip_mm"] }for each_hour in currentDay if each_hour["will_it_rain"] !=0
            ]
        sortByChanceOfRain = sorted(times,key=lambda item:item["chanceOfRain"],reverse=True)
        sortByTimes=sorted(sortByChanceOfRain)
        for each_sortedTimes in sortByTimes:
            self.stringBuilder.write(f"{each_sortedTimes["time"]}: {each_sortedTimes["chanceOfRain"]}({each_sortedTimes["precipitation"]})")

    def __str__(self):
        """
        Overrides the default '__str__' method to return rain forecast data in another format.

        :return: A formatted string displaying rain impact levels and forecasted rain times on separate lines.
        """
        return self.stringBuilder.getvalue()





