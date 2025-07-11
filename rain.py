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
        self.PRE_RAIN_WINDOW_START= self.START_TIME - self.RAIN_CHECK_HOURS_PRIOR
        self.START_TIME_FORMATTED= datetime.strptime(f"{START_TIME:02d}:00", "%H:%M").time()
        self.RAIN_CHECK_HOURS_PRIOR=RAIN_CHECK_HOURS_PRIOR
        self.RAIN_WEIGHTED_RAIN_PROBABILITY_LOW =30
        self.RAIN_WEIGHTED_RAIN_PROBABILITY_MODERATE = 50
        self.RAIN_PRECIPITATION_LOW=0.5
        self.RAIN_PRECIPITATION_MODERATE=2.0
        self.RAIN_COVERAGE_LOW= 30
        self.RAIN_COVERAGE_MODERATE=60
        self.LAST_HOUR_IMPACT_LOW=3
        self.LAST_HOUR_IMPACT_MODERATE=2

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
        string_builder = StringIO()
        time_period_forecast = self.filter_rain_metric(self.START_TIME, self.END_TIME)
        string_builder.write(f"Is rain expected: ")
        if not time_period_forecast:
            string_builder.write(f"NO (REPORT OMITTED)\n")
            return string_builder.getvalue()
        else:
            total_precipitation = self.calculate_total_precipitation(time_period_forecast)
            rain_coverage_percentage = self.calculate_rain_coverage_percentage(time_period_forecast)
            weighted_rain_probability = self.calculate_weighted_rain_probability(time_period_forecast)
            weighted_rain_probability_result = self.weighted_rain_probability_impact(weighted_rain_probability)
            rain_coverage_result=self.rain_coverage_impact(rain_coverage_percentage )
            total_precipitation_result=self.total_precipitation_impact(total_precipitation)
            number_of_hour_of_rain = len(time_period_forecast)

            string_builder.write(f"YES\n"
                                 f"Will Rain {number_of_hour_of_rain}/{self.total_hours} hours ({rain_coverage_percentage}%)"
                                 f"| Avg. Chance: {weighted_rain_probability}% | {total_precipitation} mm\n")
            string_builder.write (f"Rain Probability:{weighted_rain_probability_result}\n"
                                 f"Rain Coverage: {rain_coverage_result}\n"
                                 f"Precipitation: {total_precipitation_result}")
            string_builder.write(self.build_rain_timeline(time_period_forecast))
        return string_builder.getvalue()

    def compile_pre_window_rain_report(self):
        """
        Generates a formatted report summarizing rain conditions

        :return: A string containing the full report, structured with headers, metrics, and impact descriptions.
        """
        string_builder = StringIO()
        time_period_forecast = self.filter_rain_metric(self.PRE_RAIN_WINDOW_START, self.START_TIME)
        total_precipitation = self.calculate_total_precipitation(time_period_forecast)
        string_builder.write(f"Did It Rain {self.RAIN_CHECK_HOURS_PRIOR} hours before {self.START_TIME}:00?: ")
        if not (time_period_forecast):
            string_builder.write(f"NO (REPORT OMITTED)\n")
        else:
            last_rain_hour = (time_period_forecast[-1]["time"])
            impact= self.assess_pre_window_impact(last_rain_hour)
            string_builder.write(f"YES\n"
                                 f"Rained {len(time_period_forecast)}/{self.RAIN_CHECK_HOURS_PRIOR} last hours (Last {last_rain_hour}) | "
                                 f"{total_precipitation} mm\n")
            string_builder.write(f"Impact: {impact}\n")
            string_builder.write(self.build_rain_timeline(time_period_forecast))
        return string_builder.getvalue()

    def assess_pre_window_impact(self,last_rain_hour):
        """
        Assesses the last rainfall event and calculates the time difference (in hours) from the assigned start time,
        classifying it into one of three impact levels.

        :param last_rain_hour:  The last recorded hour of rainfall formatted in military time

        :return: A string describing the most recent rainfall before the assigned start time, including its impact level
        """
        datetime_conversion = datetime.strptime(f"{last_rain_hour}", "%H:%M").time()
        datetime_difference= datetime.combine(datetime.today(), self.START_TIME_FORMATTED) - datetime.combine(datetime.today(),datetime_conversion)
        rain_time_difference_hours= datetime_difference.total_seconds() / 3600
        if (rain_time_difference_hours > self.LAST_HOUR_IMPACT_LOW):
            return ("🟩 LOW (PLAYABLE)")
        elif (rain_time_difference_hours == self.LAST_HOUR_IMPACT_MODERATE):
            return ("🟨 MODERATE (DELAY START/CHECK COURT CONDITIONS)")
        else:
            return ("🟥 HIGH (POSTPONE)")
    def weighted_rain_probability_impact(self,weighted_rain_probability):
        """
        Classifies weighted rain probability into three impact levels

        :param weighted_rain_probability: The average chance of rain (%) during the assigned time period.

        :return: A string describing the day's rain probability, including the impact level.
        """
        if (weighted_rain_probability <self.RAIN_WEIGHTED_RAIN_PROBABILITY_LOW):
            return ("🟩 LOW (PLAYABLE)")
        elif (weighted_rain_probability <self.RAIN_WEIGHTED_RAIN_PROBABILITY_MODERATE):
            return ("🟨 MODERATE (CAUTION)\n")
        else:
            return ("🟥 HIGH (UNPLAYABLE)\n")

    def rain_coverage_impact(self, rain_coverage):
        """
        Classifies the percentage of total hours with rain into three impact levels

        :param rain_coverage: The percentage of total hours with rain forecasted.

        :return: A string describing the day's rain coverage, including the impact level.
        """
        if (rain_coverage< self.RAIN_COVERAGE_LOW):
            return ("🟩 LOW (PLAYABLE)")
        elif (rain_coverage < self.RAIN_COVERAGE_MODERATE):
            return ("🟨 MODERATE (CAUTION)\n")
        else:
            return ("🟥 HIGH (UNPLAYABLE)\n")

    def total_precipitation_impact(self,total_precipitation):
        """
        Classifies precipitation levels into three impact categories and generates an hourly timeline of rainfall amounts.

        :param total_precipitation: An integer representing the maximum precipitation (mm) in the forecast data.

        :return: A string describing the day's rainfall conditions, including the impact level classification.
        """
        if (total_precipitation<self.RAIN_PRECIPITATION_LOW):
            return (f"🟩 LOW (VERY LIGHT RAIN) \n")
        elif (total_precipitation<self.RAIN_PRECIPITATION_MODERATE):
            return ("🟨 MODERATE (LIGHT RAIN)\n")
        else:
            return ("🟥 HIGH (HEAVY RAIN)\n")

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







