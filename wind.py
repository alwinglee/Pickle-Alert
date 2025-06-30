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
        self.METRIC_LIST=[]
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

        for each_key in list(timeline[0].keys())[1:]:
            self.METRIC_LIST.append(each_key)

        return timeline[self.START_TIME:self.END_TIME]

    def find_max_wind_metric(self,time_period_forecast,metric):
        """
        Identifies the highest wind speed or wind gust from the forecast data list.

        :param time_period_forecast: List of rain data by time slice
        :param metric: String parameter representing the metric keyword (ex. "speed" or "gust")

        :return: Integer value of the highest recorded value for the specified metric in the forecast data.
        """
        max_wind=max(each_hour[f"{metric}"] for each_hour in time_period_forecast)
        return max_wind

    def calculate_average_wind_metric(self,time_period_forecast,metric):
        """
        Calculates the average wind metric value from forecast data.

        :param time_period_forecast: List of wind data by time interval.
        :param metric: String representing the wind metric to average (e.g., "speed" or "gust").

        :return: Integer value of the average for the specified wind metric.
        """
        total_sum = sum(each_hour[f"{metric}"] for each_hour in time_period_forecast)
        return round(total_sum/len(time_period_forecast))

    def compile_wind_report(self):
        """
        Generates a formatted report summarizing temperature conditions

        :return: A string containing the full report, structured with headers, metrics, and impact descriptions.
        """
        time_period_forecast=self.filter_wind_metrics()
        for metric in self.METRIC_LIST:
            display_metric_title = metric.replace("_", " ")
            average = self.calculate_average_wind_metric(time_period_forecast,metric)
            max = self.find_max_wind_metric(time_period_forecast,metric)
            impact = {"speed": self.wind_speed_impact(max),
                      "gust": self.wind_gust_impact(max)}
            self.string_builder.write (f"\n- - - WIND {display_metric_title.upper()} REPORT - - -\n"
                                        f"Max. {max} kph | Avg. {average} kph \n")
            self.string_builder.write(f"Impact: {impact[metric]}\n")
            self.build_wind_timeline(time_period_forecast,metric)
        return self.string_builder.getvalue()

    def wind_speed_impact(self,max_wind_speed):
        """
        Generates a summary of the wind speed conditions for the day, including impact assessments.

        :param max_wind_speed: An integer representing the highest wind speed in the forecast data.

        :return: A string describing the day's wind speed conditions, including the impact level.
        """
        if (max_wind_speed <= self.WIND_SPEED_IDEAL):
            return (f"IDEAL\n"
                    f"Description: BALL TRAVELS NORMALLY ")
        if (max_wind_speed <= self.WIND_SPEED_CHALLENGING):
            return (f"PLAYABLE BUT CHALLENGING\n"
                    f"Description: BALL MAY DRIFT")
        elif (max_wind_speed < self.WIND_SPEED_DIFFICULT):
            return (f"DIFFICULT\n"
                    f"Description: STRONG BALL DRIFT")
        else:
            return (f"IMPOSSIBLE\n"
                    f"Description: PLAY INDOORS")

    def wind_gust_impact(self,max_wind_gust):
        """
        Generates a summary of the wind gust conditions for the day, including impact assessments.

        :param max_wind_gust: An integer representing the highest wind gust in the forecast data.

        :return: A string describing the day's wind gust conditions, including the impact level.
        """
        if (max_wind_gust <= self.WIND_GUST_MINIMAL):
            return (f"MINIMAL\n"
                    f"Description: BALL TRAVELS NORMALLY ")
        elif (max_wind_gust <= self.WIND_GUST_MODERATE):
            return (f"MODERATE\n"
                    f"Description: OCCASIONAL UNPREDICTABLE DRIFT")
        elif (max_wind_gust <= self.WIND_GUST_MAXIMUM):
            return (f"MAXIMUM\n"
                    f"Description: SUDDEN UNPREDICTABLE BALL DEFLECTION")
        else:
            return (f"BEYOND MAXIMUM\n" 
                    f"Description: PLAY INDOORS")

    def build_wind_timeline(self,time_period_forecast,metric):
        """
        Generates hourly wind forecast data formatted as a chronological timeline.

        Each entry includes:
        - Time (in `HH:MM` format)
        - Wind speed (kph) or wind gust (kph)

        :return: None
        """
        self.string_builder.write(
            f"- - - TOP {self.TOP_TIMELINE_COUNT} PEAK {metric.upper()} HOURS - - -\n")
        sort_by_max = sorted(time_period_forecast, key=lambda item: item[f"{metric}"], reverse=True)[:self.TOP_TIMELINE_COUNT]
        sort_by_time = sorted(sort_by_max, key=lambda item: item["time"])
        for each_hour in sort_by_time:
                self.string_builder.write(f"\t{each_hour["time"]}: {each_hour[f"{metric}"]} kph\n")





