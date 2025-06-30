from io import StringIO
from datetime import datetime

class Temperature:
    def __init__(self,weather_data, START_TIME,END_TIME,TOP_TIMELINE_COUNT):
        self.weather_data=weather_data
        self.START_TIME=START_TIME
        self.END_TIME=END_TIME+1
        self.TOP_TIMELINE_COUNT=TOP_TIMELINE_COUNT
        self.string_builder=StringIO()
        self.METRIC_LIST=["apparent_temperature","heat_index","uv_index"]
        self.FEELS_LIKE_IDEAL = 20
        self.FEELS_LIKE_CHALLENGING = 30
        self.FEELS_LIKE_DIFFICULT = 35
        self.UV_INDEX_LOW = 2
        self.UV_INDEX_MODERATE= 5
        self.UV_INDEX_HIGH = 7
        self.UV_INDEX_VERY_HIGH = 10
        self.HEAT_INDEX_LOW = 25
        self.HEAT_INDEX_MODERATE = 32
        self.HEAT_INDEX_HIGH = 38
        self.HEAT_INDEX_VERY_HIGH = 35

    def filter_temperature_metrics(self):
        """
        Generates an hourly list within a specified time period and extracts key temperature metrics

        Each entry contains the following key-value pairs:
            - Time
            - Apparent Temperature
            - Heat Index
            - Uv Index

        :return: A time-sliced list of key temperature metrics.
        """
        hourly = self.weather_data["forecast"]["forecastday"][0]["hour"]
        timeline = [
            {"time": datetime.strptime(each_hour["time"], ("%Y-%m-%d %H:%M")).strftime("%H:%M"),
             "apparent_temperature": round(each_hour["feelslike_c"]), "heat_index":round(each_hour["heatindex_c"]),
             "uv_index":round(each_hour["uv"])} for each_hour in hourly
        ]
        return timeline[self.START_TIME:self.END_TIME]

    def find_max_temperature_metric(self, time_period_forecast, metric):
        """
        Identifies the highest temperature metric from the forecast data list.

        :param time_period_forecast: List of rain data by time slice
        :param metric: String parameter representing the metric keyword (ex. "apparent temperature" or "heat index")

        :return: Integer value of the highest recorded value for the specified metric in the forecast data.
        """
        max_raw_temperature = max(each_hour[f"{metric}"] for each_hour in time_period_forecast)
        return max_raw_temperature

    def calculate_average_temperature_metric(self,time_period_forecast,metric):
        """
        Calculates the average temperature metric value from forecast data.

        :param time_period_forecast: List of wind data by time interval.
        :param metric: String representing the temperature metric to average (e.g., "apparent temperature" or "heat index").

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
        for metric in self.METRIC_LIST:
            display_metric_title = metric.replace("_", " ")
            average = self.calculate_average_temperature_metric(time_period_forecast,metric)
            max = self.find_max_temperature_metric(time_period_forecast,metric)
            impact = {"apparent_temperature": self.apparent_temperature_impact(max),
                      "heat_index": self.heat_index_impact(max),
                      "uv_index": self.uv_index_impact(max)}
            self.string_builder.write (f"\n- - - {display_metric_title.upper()} REPORT - - -\n"
                                        f"Max. {max} | Avg. {average} \n")
            self.string_builder.write(f"Impact: {impact[metric]}\n")
            self.build_temperature_timeline(time_period_forecast,metric)
        return self.string_builder.getvalue()

    def apparent_temperature_impact(self, max_apparent_temperature):
        """
        Generates a summary of the apparent temperature conditions for the day, including impact assessments.

        :param max_apparent_temperature: An integer representing the highest apparent temperature in the forecast data.

        :return: A string describing the day's apparent temperature conditions, including the impact level.
        """
        if (max_apparent_temperature<= self.FEELS_LIKE_IDEAL):
            return (f"IDEAL\n"
                    f"Description: COMFORTABLE TEMPERATURE FOR OUTDOOR PLAY.")
        if (max_apparent_temperature <= self.FEELS_LIKE_CHALLENGING):
            return (f"PLAYABLE BUT WARM\n"
                    f"Description: HYDRATE FREQUENTLY. TAKE BREAKS.")
        elif (max_apparent_temperature < self.FEELS_LIKE_DIFFICULT):
            return (f"RISKY\n"
                    f"Description: HIGH EXERTION RISK AND SHORTEN GAMES. CONSIDER PLAYING INDOORS.")
        else:
            return (f"DANGEROUS\n"
                    f"Description: RISK OF HEATSTROKE. PLAY INDOORS.")
    def heat_index_impact(self, max_heat_index):
        """
        Generates a summary of the heat index conditions for the day, including impact assessments.

        :param max_heat_index: An integer representing the highest heat index in the forecast data.

        :return: A string describing the day's heat index conditions, including the impact level.
        """
        if (max_heat_index <= self.FEELS_LIKE_IDEAL):
            return (f"IDEAL\n"
                    f"\tDescription: COMFORTABLE TEMPERATURE FOR OUTDOOR PLAY.")
        if (max_heat_index <= self.FEELS_LIKE_CHALLENGING):
            return (f"PLAYABLE BUT WARM\n"
                    f"Description: HYDRATE FREQUENTLY. TAKE BREAKS.")
        elif (max_heat_index < self.FEELS_LIKE_DIFFICULT):
            return (f"RISKY\n"
                    f"Description: HIGH EXERTION RISK AND SHORTEN GAMES. CONSIDER PLAYING INDOORS.")
        else:
            return (f"DANGEROUS\n"
                    f"Description: RISK OF HEATSTROKE. PLAY INDOORS.")
    def uv_index_impact(self,max_uv_index):
        """
       Generates a summary of the UV index conditions for the day, including impact assessments.

       :param max_uv_index: An integer representing the highest UV index in the forecast data.

       :return: A string describing the day's uv index conditions, including the impact level.
       """
        if (max_uv_index<= self.UV_INDEX_LOW):
            return (f"LOW\n"
                    f"Description: MINIMAL RISK. BURN TIME OF 60 MINS.")
        if  (max_uv_index <= self.UV_INDEX_MODERATE):
            return (f"MODERATE\n"
                    f"Description: WEAR SPF 30+ SUNSCREEN. BURN TIME OF 45 MINS.")
        elif (max_uv_index < self.UV_INDEX_HIGH):
            return (f"HIGH\n"
                    f"Description: WEAR SPF 50+ SUNSCREEN. BURN TIME OF 30 MINS")
        elif (max_uv_index < self.UV_INDEX_VERY_HIGH):
            return (f"VERY HIGH\n"
                    f"Description: LIMIT SESSION TO 1-2 HOURS. BURN TIME OF 20 MINS")
        else:
            return (f"EXTREME\n"
                    f"Description: RESCHEDULE PICKEBALL SESSION OR PLAY INDOORS. BURN TIME OF 10 MINS")

    def build_temperature_timeline(self,time_period_forecast, metric):
        """
        Generates hourly temperature forecast data formatted as a chronological timeline.

        Each entry includes:
        - Time (in `HH:MM` format)
        - Apparent Temperature (°C), Heat Index (°C), or UV Index (lvl.)

        :return: None
        """
        display_metric_name= metric.replace("_"," ")
        self.string_builder.write(f"- - - TOP {self.TOP_TIMELINE_COUNT} PEAK {display_metric_name.upper()} HOURS - - -\n")
        sort_by_max= sorted(time_period_forecast, key=lambda item:item[f"{metric}"],reverse=True)[:self.TOP_TIMELINE_COUNT]
        sort_by_time = sorted(sort_by_max,key=lambda item:item["time"])
        for each_hour in sort_by_time:
            if (metric == "uv_index"):
                self.string_builder.write(f"\t{each_hour["time"]}: lvl. {each_hour[f"{metric}"]} \n")
            else:
                self.string_builder.write(f"\t{each_hour["time"]}: {each_hour[f"{metric}"]} °C\n")






