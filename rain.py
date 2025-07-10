from io import StringIO
from datetime import datetime
class Rain:
    """
    A class to filter, analyze, and report rain-related weather data.
    """
    def __init__(self,weather_data,START_TIME, END_TIME, TOP_TIMELINE_COUNT, RAIN_CHECK_HOURS_PRIOR,total_hours):
        """
        Initializes the Rain class with key rain-related metrics from an API response and sets evaluation thresholds
        for rain impact levels.

        :param weather_data: Weather forecast response in JSON format.

        :return: None
        """
        self.weather_data=weather_data
        self.METRIC_LIST=[]
        self.START_TIME=START_TIME
        self.END_TIME=END_TIME
        self.total_hours=total_hours
        self.TOP_TIMELINE_COUNT = TOP_TIMELINE_COUNT
        self.RAIN_CHECK_HOURS_PRIOR=RAIN_CHECK_HOURS_PRIOR
        self.RAIN_CHANCE_LOW_THRESH=30
        self.RAIN_CHANCE_HIGH_THRESH = 50
        self.RAIN_PRECIPITATION_LOW_THRESH=2.5
        self.RAIN_PRECIPITATION_MODERATE_THRESH=7.5

    def filter_rain_metric(self,START_TIME,END_TIME):
        """
        Generates an hourly list within a specified time period and extracts key rain metrics

        Each entry contains the following key-value pairs:
            - Time
            - chance of rain (percentage)
            - Expected precipitation amount (mm)

        :return: A time-sliced list of key rain metrics.
        """
        hourly = self.weather_data["forecast"]["forecastday"][0]["hour"]
        self.METRIC_LIST=[]
        timeline = []
        format_start_time = datetime.strptime(f"{START_TIME:02d}:00", "%H:%M").time()
        format_end_time = datetime.strptime(f"{END_TIME:02d}:00", "%H:%M").time()

        for each_hour in hourly:
            format_time =  datetime.strptime(each_hour["time"],"%Y-%m-%d %H:%M").time()

            # Only includes hours where rain is expected (API uses 1 = Yes)
            if (format_time>= format_start_time and format_time <=format_end_time) and each_hour["will_it_rain"]==1:
                timeline.append({
                    "time": format_time.strftime("%H:%M"),
                    "rain_percentage":each_hour["chance_of_rain"],
                    "rain_amount":each_hour["precip_mm"],
                })
        if (timeline):
            temp_list= [ each_key for each_key in timeline[0].keys()][2:]
            for each_key in temp_list:
                self.METRIC_LIST.append(each_key)
        return timeline

    def calculate_rain_coverage_percentage(self, time_period_forecast):
        """
        Calculates the percentage of hours within a time period that have rain forecasted.

        :param time_period_forecast: List of hourly rain data.

        :return: Integer percentage of hours with expected rain during the period.
        """
        return round(((len(time_period_forecast)/self.total_hours)*100))

    def calculate_weighted_rain_probability(self,time_period_forecast):
        """
        Calculates the average chance of rain across a time period

        :param time_period_forecast: List of hourly rain data.

        :return: Integer percentage of average chance of rain
        """
        rain_percentage=0
        for each_hour in time_period_forecast:
            rain_percentage+=each_hour["rain_percentage"]
        return round(rain_percentage/self.total_hours)

    def calculate_total_precipitation(self, time_period_forecast):
        """
        Calculates the average chance of rain across a time period.

        :param time_period_forecast: List of hourly rain data.

        :return: Integer representing the mean probability of rain.
        """
        total_precipitation=0
        for each_hour in time_period_forecast:
            total_precipitation+=each_hour["rain_amount"]
        return round(total_precipitation,2)

    def compile_during_window_rain_report(self):
        """
        Generates a formatted report summarizing rain conditions

        :return: A string containing the full report, structured with headers, metrics, and impact descriptions.
        """
        string_builder=StringIO()
        time_period_forecast=self.filter_rain_metric(self.START_TIME,self.END_TIME)
        string_builder.write(f"Is rain expected: ")
        if not time_period_forecast:
            string_builder.write (f"NO (REPORT OMITTED)\n")
            return string_builder.getvalue()
        else:
            total_precipitation = self.calculate_total_precipitation(time_period_forecast)
            rain_coverage_percentage = self.calculate_rain_coverage_percentage(time_period_forecast)
            weighted_rain_probability= self.calculate_weighted_rain_probability(time_period_forecast)
            number_of_hour_of_rain=len(time_period_forecast)

            string_builder.write(f"YES\n")
            string_builder.write(f"Will Rain {number_of_hour_of_rain}/{self.total_hours} hours ({rain_coverage_percentage}%) "
                                 f"| Avg. Chance: {weighted_rain_probability}% | {total_precipitation} mm\n")
            string_builder.write(self.build_rain_timeline(time_period_forecast))
        return string_builder.getvalue()

    def compile_pre_window_rain_report(self):
        """
        Generates a formatted report summarizing rain conditions

        :return: A string containing the full report, structured with headers, metrics, and impact descriptions.
        """
        string_builder=StringIO()
        time_period_forecast = self.filter_rain_metric((self.START_TIME-self.RAIN_CHECK_HOURS_PRIOR),self.START_TIME)
        total_precipitation = self.calculate_total_precipitation(time_period_forecast)
        string_builder.write(f"Precipitation last {self.RAIN_CHECK_HOURS_PRIOR} hours before {self.START_TIME}:00?: ")
        if not (time_period_forecast):
            string_builder.write(f"NO (REPORT OMITTED)\n")
        else:
            last_hour_of_rain = (time_period_forecast[-1]["time"])
            string_builder.write(f"YES\n")
            string_builder.write(f"Rained {len(time_period_forecast)}/{self.RAIN_CHECK_HOURS_PRIOR} hour (Last {last_hour_of_rain}) | "
                                 f"{total_precipitation} mm\n")
            string_builder.write(self.build_rain_timeline(time_period_forecast))
        return string_builder.getvalue()

    def chance_of_rain_impact(self,total_chance_of_rain):
        """
        Classifies rain probability into three impact levels and generates an hourly timeline of rain percentages.

        :param total_chance_of_rain: An integer representing the highest chance of rain percentage (%) in the forecast data.

        :return: A string describing the day's rain probability, including the impact level.
        """
        if (total_chance_of_rain <self.RAIN_CHANCE_LOW_THRESH):
            return ("MINIMAL RISK OF RAIN\n"
                    "Description: Courts Will Stay Dry And Rain Is Unlikely.")
        elif (total_chance_of_rain <self.RAIN_CHANCE_HIGH_THRESH ):
            return ("MODERATE RISK OF RAIN\n"
                    "Description: Possible Rain. Courts May Get Wet.")
        else:
            return ("MAXIMUM LIKELIHOOD OF RAIN\n"
                    "Description: Rain Guaranteed. Postpone play.")

    def total_precipitation_impact(self,total_precipitation):
        """
        Classifies precipitation levels into three impact categories and generates an hourly timeline of rainfall amounts.

        :param total_precipitation: An integer representing the maximum precipitation (mm) in the forecast data.

        :return: A string describing the day's rainfall conditions, including the impact level classification.
        """
        if (total_precipitation<self.RAIN_PRECIPITATION_LOW_THRESH):
            return (f"MINIMAL AMOUNT OF RAIN\n"
                    f"Description: DRIZZLE/ LIGHT RAIN. LITTLE TO NO ACCUMULATION.")
        elif (total_precipitation<self.RAIN_PRECIPITATION_MODERATE_THRESH):
            return ("MODERATE AMOUNT OF RAIN\n"
                    f"Description: STEADY RAIN. PUDDLES WILL DEVELOP.")
        else:
            return ("MAXIMUM AMOUNT OF RAIN\n"
                    f"Description: HEAVY RAINFALL.")

    def build_rain_timeline(self, time_period_forecast):
        """
        Generates hourly temperature forecast data formatted as a chronological timeline.

        Each entry includes:
        - Time (in `HH:MM` format)
        - Chance of Rain (%) or expected amount of total precipitation (mm)

        :return: None
        """
        string_builder=StringIO()
        string_builder.write(f"- - - TOP {self.TOP_TIMELINE_COUNT} PEAK RAIN HOURS - - -\n")
        sort_by_max = sorted(time_period_forecast, key=lambda item: item["rain_percentage"], reverse=True)[
                      :self.TOP_TIMELINE_COUNT]
        sort_by_time = sorted(sort_by_max, key=lambda item: item["time"])
        for each_hour in sort_by_time:
                string_builder.write(f"\t{each_hour["time"]}: {each_hour["rain_percentage"]}% ({each_hour["rain_amount"]} mm)\n")
        return string_builder.getvalue()







