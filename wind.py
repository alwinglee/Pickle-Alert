from io import StringIO
from datetime import datetime


class Wind:
    """
    A class that processes weather data, evaluates wind impact (both speed and gusts), and generates actionable reports
    """
    WIND_SPEED_LOW = 15
    WIND_SPEED_MODERATE = 25
    WIND_GUST_LOW = 20
    WIND_GUST_MODERATE = 35

    def __init__(self, top_timeline_count, hourly_selected_forecast_data):
        self.top_timeline_count = top_timeline_count
        self.hourly_selected_forecast_data = hourly_selected_forecast_data
        self.METRIC_LIST = []

    def filter_wind_metrics(self):
        """
        Generates an hourly list within a specified time period and extracts key wind metrics

        Each entry contains the following key-value pairs:
            - Time
            - Wind Speed (kph)
            - Wind Gust (kph)

        :return: A time-sliced list of key wind metrics.
        """
        timeline = [
            {"time": datetime.strptime(each_hour["time"], "%Y-%m-%d %H:%M").strftime("%H:%M"),
             "speed": round(each_hour["wind_kph"]), "gust": round(each_hour["gust_kph"])} for each_hour
            in self.hourly_selected_forecast_data
        ]
        self.METRIC_LIST = list(timeline[0].keys())[1:]
        return timeline

    def find_max_wind_metric(self, time_period_forecast, metric):
        """
        Identifies the highest wind speed or wind gust from the forecast data list.

        :param time_period_forecast: List of rain data by time slice
        :param metric: String parameter representing the metric keyword (ex. "speed" or "gust")

        :return: Integer value of the highest recorded value for the specified metric in the forecast data.
        """
        max_wind = max(each_hour[f"{metric}"] for each_hour in time_period_forecast)
        return max_wind

    def calculate_average_wind_metric(self, time_period_forecast, metric):
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
        string_builder = StringIO()
        time_period_forecast = self.filter_wind_metrics()
        for metric in self.METRIC_LIST:
            display_metric_title = metric.replace("_", " ")
            average = self.calculate_average_wind_metric(time_period_forecast, metric)
            max_value = self.find_max_wind_metric(time_period_forecast, metric)
            impact = self.select_impact_method(metric, max_value)

            string_builder.write(f"\n= = = 🍃 WIND {display_metric_title.upper()} 🍃 = = =\n"
                                 f"Max. {max_value} kph | Avg. {average} kph \n")
            string_builder.write(f"{impact}\n")
            string_builder.write(self.build_wind_timeline(time_period_forecast, metric))
        return string_builder.getvalue()

    def wind_summary(self):
        """
        Generates a summary of impact levels for all wind metrics

        :return: Formatted string with impact levels for all wind metrics
        """
        string_builder = StringIO()
        time_period_forecast = self.filter_wind_metrics()
        for metric in self.METRIC_LIST:
            display_metric_title = metric.replace("_", " ").title()
            max_value = self.find_max_wind_metric(time_period_forecast, metric)
            impact = self.select_impact_method(metric, max_value)
            string_builder.write(f"Wind {display_metric_title}: {impact}\n")
        return string_builder.getvalue()

    def wind_speed_impact(self, max_wind_speed):
        """
        Generates a summary of the wind speed conditions for the day, including impact assessments.

        :param max_wind_speed: An integer representing the highest wind speed in the forecast data.

        :return: A string describing the day's wind speed conditions, including the impact level.
        """
        if max_wind_speed <= self.WIND_SPEED_LOW:
            return f"🟩 LOW (PREDICTABLE PLAY)"
        elif max_wind_speed <= self.WIND_SPEED_MODERATE:
            return f"🟨 MODERATE (BALL SWERVE)"
        else:
            return f"🟥 HIGH (ERRATIC MOVEMENT)"

    def wind_gust_impact(self, max_wind_gust):
        """
        Generates a summary of the wind gust conditions for the day, including impact assessments.

        :param max_wind_gust: An integer representing the highest wind gust in the forecast data.

        :return: A string describing the day's wind gust conditions, including the impact level.
        """
        if max_wind_gust <= self.WIND_GUST_LOW:
            return f"🟩 LOW (PREDICTABLE PLAY)"
        elif max_wind_gust <= self.WIND_GUST_MODERATE:
            return f"🟨 MODERATE (BALL SWERVE)"
        else:
            return f"🟥 HIGH (ERRATIC MOVEMENT)"

    def build_wind_timeline(self, time_period_forecast, metric):
        """
        Generates hourly wind forecast data formatted as a chronological timeline

        Each entry includes:
        - Time (in `HH:MM` format)
        - Wind speed (kph) or wind gust (kph)

        :param time_period_forecast: List of wind data points by time interval
        :param metric: Key indicating which wind metric to display ("speed" or "gust")

        :return: Formatted string showing chronological timeline entries for the specified metric
        """
        string_builder = StringIO()
        string_builder.write(f"- - - TOP {self.top_timeline_count} PEAK {metric.upper()} HOURS - - -\n")
        sort_by_max = sorted(time_period_forecast, key=lambda item: item[f"{metric}"],
                             reverse=True)[:self.top_timeline_count]
        sort_by_time = sorted(sort_by_max, key=lambda item: item["time"])
        for each_hour in sort_by_time:
            string_builder.write(f"\t{each_hour['time']}: {each_hour[metric]} kph\n")
        return string_builder.getvalue()

    def select_impact_method(self, metric, max_value):
        """
        Selects the appropriate impact method based on the given parameters

        :param metric: Key indicating which wind metric to display ("speed" or "gust")
        :param max_value: Maximum value (integer) found in the metric dataset

        :return: String describing the impact level corresponding to the max value
        """
        method = {"speed": self.wind_speed_impact,
                  "gust": self.wind_gust_impact}
        return method[metric](max_value)
