from io import StringIO
from datetime import datetime

class Wind:
    """
    A class that processes weather data, evaluates wind impact (both speed and gusts), and generates actionable reports
    """
    def __init__(self,weather_data,START_TIME,END_TIME,TOP_TIMELINE_COUNT):
        self.string_builder = StringIO()
        self.TOP_TIMELINE_COUNT=TOP_TIMELINE_COUNT
        self.weather_data=weather_data
        self.START_TIME=START_TIME
        self.END_TIME=END_TIME+1
        self.WIND_SPEED_IDEAL = 15
        self.WIND_SPEED_CHALLENGING = 24
        self.WIND_SPEED_DIFFICULT= 32
        self.WIND_GUST_MINIMAL = 18
        self.WIND_GUST_MODERATE = 26
        self.WIND_GUST_MAXIMUM = 32

    def filter_wind_metrics(self):
        """
        Generates an hourly list within a specified time period and extracts key wind metrics

        Each entry contains the following key-value pairs:
            - Time
            - Wind Speed (kph)
            - Wind Gust (kph)

        :return: A time-sliced list of key wind metrics.
        """
        hourly = self.weather_data["forecast"]["forecastday"][0]["hour"]
        timeline = [
            {"time":datetime.strptime(each_hour["time"],("%Y-%m-%d %H:%M")).strftime("%H:%M"),
             "speed":round(each_hour["wind_kph"]), "gust":round(each_hour["gust_kph"])} for each_hour in hourly
        ]
        return timeline[self.START_TIME:self.END_TIME]

    def find_max_wind(self,time_period_forecast,metric):
        """
        Identifies the highest wind speed or wind gust from the forecast data list.

        :param time_period_forecast: List of rain data by time slice
        :param metric: String parameter representing the metric keyword (ex. "speed" or "gust")


        :return: Integer value of the highest recorded value for the specified metric in the forecast data.
        """
        max_wind= 0
        for each_hour in time_period_forecast:
            if (each_hour[f"{metric}"]>max_wind):
                max_wind=each_hour[f"{metric}"]
        return max_wind

    def wind_summary(self):
        """
        Generates a summary of the wind speed condition for the day, including impact assessments.

        :return: String containing the day's wind speed status, including impact level description when applicable
        """
        time_period_forecast=self.filter_wind_metrics()
        max_wind_speed= self.find_max_wind(time_period_forecast,"speed")
        max_wind_gust=self.find_max_wind(time_period_forecast,"gust")
        return ("WIND SPEED:\n"
                f"Playability: {self.wind_speed_impact(max_wind_speed)}\n"
                f"\nWIND GUST:\n"
                f"{self.wind_gust_impact(max_wind_gust)}\n")

    def wind_speed_impact(self,max_wind_speed):
        if (max_wind_speed <= self.WIND_SPEED_IDEAL):
            return (f"IDEAL (max.{max_wind_speed}kph)\n"
                    f"Description: BALL TRAVELS NORMALLY ")
        elif (max_wind_speed <= self.WIND_SPEED_CHALLENGING):
            self.build_wind_timeline("speed")
            return (f"PLAYABLE BUT CHALLENGING (max.{max_wind_speed}kph)\n"
                    f"Description: BALL MAY DRIFT")
        elif (max_wind_speed < self.WIND_SPEED_DIFFICULT):
            self.build_wind_timeline("speed")
            return (f"DIFFICULT (max.{max_wind_speed}kph)\n"
                    f"Description: STRONG BALL DRIFT")
        else:
            self.build_wind_timeline("speed")
            return (f"Playability: IMPOSSIBLE (max.{max_wind_speed}kph)\n"
                    f"Description: PLAY INDOORS")


    def wind_gust_impact(self,max_wind_gust):
        """
        Generates a summary of the wind gust condition for the day, including impact assessments.

        :return: String containing the day's wind gust status, including impact level description when applicable
        """
        if (max_wind_gust <= self.WIND_GUST_MINIMAL):
            return (f"Impact: MINIMAL (max.{max_wind_gust}kph)\n"
                    f"Description: BALL TRAVELS NORMALLY ")
        elif (max_wind_gust <= self.WIND_GUST_MODERATE):
            self.build_wind_timeline("gust")
            return (f"Impact: MODERATE (max.{max_wind_gust}kph)\n"
                    f"Description: OCCASIONAL UNPREDICTABLE DRIFT")
        elif (max_wind_gust <= self.WIND_GUST_MAXIMUM):
            self.build_wind_timeline("gust")
            return (f"Impact: MAXIMUM (max.{max_wind_gust}kph)\n"
                    f"Description: SUDDEN UNPREDICTABLE BALL DEFLECTION")
        else:
            self.build_wind_timeline("gust")
            return (f"IMPACT: BEYOND MAXIMUM (max.{max_wind_gust}kph)\n" 
                    f"Description: PLAY INDOORS")

    def build_wind_timeline(self,metric):
        """
        Generates hourly wind forecast data formatted as a chronological timeline.

        Each entry includes:
        - Time (in `HH:MM` format)
        - Wind speed (kph) or wind gust (kph)

        :return: None
        """
        self.string_builder.write(f"\n- - - WIND {metric.upper()} REPORT - - -\n"
                                 f"Top {self.TOP_TIMELINE_COUNT} Peak Wind {metric.title()} Hours:\n")
        sort_by_max= sorted(self.filter_wind_metrics(), key=lambda item:item[f"{metric}"],reverse=True)[:self.TOP_TIMELINE_COUNT]
        sort_by_time = sorted(sort_by_max,key=lambda item:item["time"])
        for each_hour in sort_by_time:
            self.string_builder.write(f"\t{each_hour["time"]}: {each_hour[f"{metric}"]} kph\n")

    def __str__(self):
        """
        Overrides the default '__str__' method to return wind forecast data in another format.

        :return: A formatted string displaying wind impact levels and forecasted wind times on separate lines.
        """
        return self.string_builder.getvalue()






