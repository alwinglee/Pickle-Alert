from io import StringIO
from datetime import datetime

class Temperature:
    """
    A class that processes weather data, evaluates temperature, humidity, and UV index, and generates actionable reports.
    """
    def __init__(self,top_timeline_count,hourly_selected_forecast_data):
        self.top_timeline_count = top_timeline_count
        self.hourly_selected_forecast_data = hourly_selected_forecast_data
        self.METRIC_LIST = []
        self.FEELS_LIKE_LOW = 24
        self.FEELS_LIKE_MODERATE = 33
        self.UV_INDEX_LOW = 2
        self.UV_INDEX_MODERATE = 5
        self.UV_INDEX_HIGH = 7
        self.UV_INDEX_VERY_HIGH = 10
        self.HEAT_INDEX_LOW = 25
        self.HEAT_INDEX_MODERATE = 33
        self.HUMIDITY_LOW = 30
        self.HUMIDITY_MODERATE = 60
        self.HUMIDITY_HIGH = 75

    def filter_temperature_metrics(self):
        """
        Generates an hourly list within a specified time period and extracts key temperature metrics

        Each entry contains the following key-value pairs:
            - Time
            - feels like
            - Uv Index

        :return: A time-sliced list of key temperature metrics.
        """
        timeline = [
            {"time": datetime.strptime(each_hour["time"], ("%Y-%m-%d %H:%M")).strftime("%H:%M"),
             "feels_like": round(each_hour["feelslike_c"]), "humidity": each_hour["humidity"],
             "uv_index": round(each_hour["uv"])} for each_hour in self.hourly_selected_forecast_data
        ]
        self.METRIC_LIST = list(timeline[0].keys())[1:]
        return timeline

    def find_max_temperature_metric(self, time_period_forecast, metric):
        """
        Identifies the highest temperature metric from the forecast data list.

        :param time_period_forecast: List of rain data by time slice
        :param metric: String parameter representing the metric keyword (ex. "feels like" or "UV index")

        :return: Integer value of the highest recorded value for the specified metric in the forecast data.
        """
        max_raw_temperature = max(each_hour[f"{metric}"] for each_hour in time_period_forecast)
        return max_raw_temperature

    def calculate_average_temperature_metric(self,time_period_forecast,metric):
        """
        Calculates the average temperature metric value from forecast data.

        :param time_period_forecast: List of wind data by time interval.
        :param metric: String representing the temperature metric to average (e.g., "feels like" or "UV index").

        :return: Integer value of the average for the specified temperature metric.
        """
        total_sum = sum(each_hour[f"{metric}"] for each_hour in time_period_forecast)
        return round(total_sum/len(time_period_forecast))


    def compile_temperature_report(self):
        """
        Generates a formatted report summarizing temperature conditions

        :return: A string containing the full report, structured with headers, metrics, and impact descriptions.
        """
        time_period_forecast=self.filter_temperature_metrics()
        string_builder = StringIO()
        for metric in self.METRIC_LIST:
            display_metric_title = metric.replace("_", " ")
            average = self.calculate_average_temperature_metric(time_period_forecast,metric)
            max = self.find_max_temperature_metric(time_period_forecast,metric)
            impact = self.select_impact_method(metric,max)

            string_builder.write (f"\n= = = ☀️ {display_metric_title.upper()} ☀️ = = =\n")
            if metric=="uv_index":
                string_builder.write(f"Max. index {max}  | Avg. index {average}\n")
            elif metric=="humidity":
                string_builder.write(f"Max. {max} % | Avg. {average} %\n")
            else:
                string_builder.write(f"Max. {max} °C | Avg. {average} °C \n")
            string_builder.write(f"{impact}\n")
            string_builder.write(self.build_temperature_timeline(time_period_forecast,metric))
        return string_builder.getvalue()

    def temperature_summary(self):
        """
        Generates a summary of impact levels for all temperature metrics

        :return: Formatted string with impact levels for temperature metrics
        """
        string_builder=StringIO()
        time_period_forecast=self.filter_temperature_metrics()
        for metric in self.METRIC_LIST:
            display_metric_title = metric.replace("_", " ").title()
            max = self.find_max_temperature_metric(time_period_forecast, metric)
            impact = self.select_impact_method(metric,max)
            string_builder.write(f"{display_metric_title}: {impact}\n")
        return string_builder.getvalue()

    def feels_like_impact(self, max_feels_like):
        """
        Generates a summary of the feels like conditions for the day, including impact assessments.

        :param max_feels_like: An integer representing the highest feels like in the forecast data.

        :return: A string describing the day's feels like conditions, including the impact level.
        """
        if (max_feels_like<= self.FEELS_LIKE_LOW):
            return (f"🟩 LOW (COMFORTABLE)")
        elif (max_feels_like <= self.FEELS_LIKE_MODERATE):
            return (f"🟨 MODERATE (HEAT FATIGUE)")
        else:
            return (f"🟥 HIGH (DANGEROUS HEAT)")

    def uv_index_impact(self,max_uv_index):
        """
       Generates a summary of the UV index conditions for the day, including impact assessments.

       :param max_uv_index: An integer representing the highest UV index in the forecast data.

       :return: A string describing the day's uv index conditions, including the impact level.
       """
        if (max_uv_index<= self.UV_INDEX_LOW):
            return (f"🟩 LOW (60 MIN. BURN TIME)")
        elif  (max_uv_index <= self.UV_INDEX_MODERATE):
            return (f"🟨 MODERATE (45 MIN. BURN TIME)")
        elif (max_uv_index < self.UV_INDEX_HIGH):
            return (f"🟥 HIGH (30 MIN. BURN TIME)")
        elif (max_uv_index < self.UV_INDEX_VERY_HIGH):
            return (f"🟥 VERY HIGH (15 MIN. BURN TIME)")
        else:
            return (f"🟥 EXTREME (STAY INDOORS)")

    def humidity_impact(self, max_humidity):
        """
       Generates a summary of the humidity conditions for the day, including impact assessments.

       :param max_humidity: An integer representing the highest humidity in the forecast data.

       :return: A string describing the day's humidity conditions, including the impact level.
       """
        if (max_humidity <= self.HUMIDITY_LOW):
            return (f"🟩 LOW (FAST DEHYDRATION)")
        elif (max_humidity <= self.HUMIDITY_MODERATE):
            return (f"🟨 MODERATE (COMFORTABLE)")
        elif (max_humidity< self.HUMIDITY_HIGH):
            return (f"🟥 HIGH (AIR FEELS STICKY)")
        else:
            return (f"🟥 EXTREME (EXHAUSTION RISK)")

    def build_temperature_timeline(self,time_period_forecast, metric):
        """
        Generates hourly temperature forecast data formatted as a chronological timeline

        Each entry includes:
        - Time (in `HH:MM` format)
        - feels like (°C) or UV Index (index.)

        :param time_period_forecast: List of wind data points by time interval
        :param metric: Key indicating which wind metric to display ("feels_like","heat_index", or "uv_index")

        :return: Formatted string showing chronological timeline entries for the specified metric
        """
        string_builder = StringIO()
        display_metric_name= metric.replace("_"," ")
        string_builder.write(f"- - - TOP {self.top_timeline_count} PEAK {display_metric_name.upper()} HOURS - - \n")
        sort_by_max= sorted(time_period_forecast, key=lambda item:item[f"{metric}"],reverse=True)[:self.top_timeline_count]
        sort_by_time = sorted(sort_by_max,key=lambda item:item["time"])
        for each_hour in sort_by_time:
            if (metric == "uv_index"):
                string_builder.write(f"\t{each_hour["time"]}: Index {each_hour[f"{metric}"]} \n")
            elif(metric=="humidity"):
                string_builder.write(f"\t{each_hour["time"]}: {each_hour[f"{metric}"]} % \n")
            else:
                string_builder.write(f"\t{each_hour["time"]}: {each_hour[f"{metric}"]} °C\n")
        return string_builder.getvalue()

    def select_impact_method(self, metric, max):
        """
        Selects the appropriate impact method based on the given parameters.

        :param metric: Key indicating which temperature metric to display ("feels like", "humidity", or "uv index")
        :param max: Maximum value (integer) found in the metric dataset

        :return: String describing the impact level corresponding to the max value
        """
        method = {"feels_like": self.feels_like_impact,
                  "humidity":self.humidity_impact,
                  "uv_index":self.uv_index_impact}
        return method[metric](max)






