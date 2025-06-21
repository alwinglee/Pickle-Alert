from io import StringIO
from datetime import datetime
class Rain:
    """
    A class to filter, analyze, and report rain-related weather data.
    """
    def __init__(self,weather_data,START_TIME, END_TIME, TOP_TIMELINE_TIME):
        """
        Initializes the Rain class with key rain-related metrics from an API response and sets evaluation thresholds
        for rain impact levels.

        :param weather_data: Weather forecast response in JSON format.

        :return: None
        """
        self.weather_data=weather_data
        self.string_builder = StringIO()
        self.START_TIME=START_TIME
        self.END_TIME=END_TIME+1
        self.TOP_TIMELINE_TIME=TOP_TIMELINE_TIME
        self.RAIN_CHANCE_LOW_THRESH=30
        self.RAIN_CHANCE_HIGH_THRESH = 50
        self.RAIN_PRECIPITATION_LOW_THRESH=2.5
        self.RAIN_PRECIPITATION_MODERATE_THRESH=7.5

    def filter_rain_metric(self):
        """
        Generates an hourly list within a specified time period and extracts key rain metrics

        Each entry contains the following key-value pairs:
            - Time
            - chance of rain (percentage)
            - Expected precipitation amount (mm)

        :return: A time-sliced list of key rain metrics.
        """
        hourly = self.weather_data["forecast"]["forecastday"][0]["hour"]
        timeline = [
            {"time":datetime.strptime(each_hour["time"],("%Y-%m-%d %H:%M")).strftime("%H:%M"),
             "rain_percentage":each_hour["chance_of_rain"],
             "rain_amount":each_hour["precip_mm"]} for each_hour in hourly if each_hour["will_it_rain"]==1
        ]
        return timeline[self.START_TIME:self.END_TIME]

    def calculate_rain_percentage(self, time_period_forecast):
        """
        Calculates the probability of rain occurring during a given time period.

        :param time_period_forecast: List of rain data by time slice.

        :return: String containing the day's rain status, including impact level description when applicable.
        """
        total=1
        for each_rain_percentage in time_period_forecast["rain_percentage"]:
            total*=(1-(each_rain_percentage/100))
        calculation = (1-total)*100
        return calculation

    def calculate_total_precipitation(self, time_period_forecast):
        """
        Calculates the total expected precipitation (in mm) for the specified time period.

        :param time_period_forecast: List of rain data by time slice.

        :return: Integer representing the total expected precipitation during the time period.
        """
        total_precipitation=0
        for each_hour in time_period_forecast:
            total_precipitation+=each_hour["rain_amount"]
        return round(total_precipitation)

    def rain_summary(self):
        """
        Generates a summary of the rain condition for the day, including impact assessments.

        :return: String containing the day's rain status, including impact level description when applicable.
        """
        time_period_forecast = self.filter_rain_metric()
        if (len(time_period_forecast)==0):
            return (f"Will It Rain During This Period?: NO")
        else:
            total_precipitation = self.calculate_total_precipitation(time_period_forecast)
            total_chance_of_rain = self.calculate_rain_percentage(time_period_forecast)
            return(f"Will It Rain During This Period?: YES\n"
                  f"- Chance of Rain: {self.chance_of_rain_impact(total_chance_of_rain)}({total_chance_of_rain}% over {self.END_TIME-self.START_TIME} hours)\n"
                  f"- Precipitation: {self.total_precipitation_impact(total_precipitation)} (Max.{total_precipitation}mm)\n")

    def chance_of_rain_impact(self,total_chance_of_rain):
        """
        Classifies rain probability into three impact levels and calls another function to generate an hourly timeline
        of rain percentages.

        :return: String containing the impact level and description.
        """
        if (total_chance_of_rain <self.RAIN_CHANCE_LOW_THRESH):
            return ("MINIMAL RISK OF RAIN\n"
                    "- Description: Courts Will Stay Dry And Rain Is Unlikely.")
        elif (total_chance_of_rain <self.RAIN_CHANCE_HIGH_THRESH ):
            self.build_rain_timeline("rain_percentage","%")
            return ("MODERATE RISK OF RAIN\n"
                    "- Description: Possible Rain. Courts May Get Wet.")
        else:
            self.build_rain_timeline("rain_percentage","%")
            return ("MAXIMUM LIKELIHOOD OF RAIN\n"
                    "- Description: Rain Guaranteed. Postpone play.")

    def total_precipitation_impact(self,total_precipitation):
        """
        Classifies rain probability into three impact levels and calls another function to generate an hourly timeline
        of rain amount.

        :return: String containing the impact level and description.
        """
        if (total_precipitation<self.RAIN_PRECIPITATION_LOW_THRESH):
            return (f"MINIMAL AMOUNT OF RAIN"
                    f"- Description: DRIZZLE/ LIGHT RAIN. LITTLE TO NO ACCUMULATION.")
        elif (total_precipitation<self.RAIN_PRECIPITATION_MODERATE_THRESH):
            self.build_rain_timeline("rain_amount", "mm")
            return ("MODERATE AMOUNT OF RAIN"
                    f"- Description: STEADY RAIN. PUDDLES WILL DEVELOP.")
        else:
            self.build_rain_timeline("rain_amount", "mm")
            return ("MAXIMUM AMOUNT OF RAIN"
                    f"- Description: HEAVY RAINFALL.")

    def build_rain_timeline(self,metric,units):
        """
        Generates hourly rain forecast data formatted as a chronological timeline.

        Each entry includes:
            - Time (HH:MM format)
            - Chance of rain (percentage) or Expected precipitation amount (mm)

        return: None
        """
        timeline=self.filter_rain_metric()
        self.string_builder.write(f"- - - RAIN {metric} REPORT - - -\n"
                                  f"Top {self.TOP_TIMELINE_TIME} Peak Rain {metric} Hours")
        sort_by_max = sorted(timeline,key=lambda item:item[f"{metric}"],reverse=True)
        sort_by_time=sorted(sort_by_max,key=lambda item:item["time"])
        for each_hour in sort_by_time:
            self.string_builder.write(f"\t {each_hour["time"]}: {each_hour[f"{metric}"]} {units}")

    def __str__(self):
        """
        Overrides the default '__str__' method to return rain forecast data in another format.

        :return: A formatted string displaying rain impact levels and forecasted rain times on separate lines.
        """
        return self.string_builder.getvalue()





