from io import StringIO
from datetime import datetime


class Rain:
    """
    A class to filter, analyze, and report rain-related weather data.
    """
    RAIN_WEIGHTED_RAIN_PROBABILITY_LOW = 30
    RAIN_WEIGHTED_RAIN_PROBABILITY_MODERATE = 50
    RAIN_PRECIPITATION_LOW = 0.5
    RAIN_PRECIPITATION_MODERATE = 2.0
    RAIN_COVERAGE_LOW = 30
    RAIN_COVERAGE_MODERATE = 60
    LAST_HOUR_IMPACT_LOW = 3
    LAST_HOUR_IMPACT_MODERATE = 2

    def __init__(self, start_time, end_time, top_timeline_count, rain_check_hours_prior, forecast_data):
        self.start_time = start_time
        self.end_time = end_time
        self.duration = end_time-start_time
        self.top_timeline_count = top_timeline_count
        self.rain_check_hours_prior = rain_check_hours_prior
        self.pre_rain_window_start = self.start_time - self.rain_check_hours_prior
        self.forecast_data = forecast_data

    def convert_to_datetime(self, time):
        """
        Converts an integer time value (start_time or end_time) to a datetime object.

        :param time: An integer representing either the start time or end time in hours (24-hour format)

        :return: A datetime object formatted to display military time (hours and minutes)
        """
        return datetime.strptime("23:59" if time == 24 else f"{time:02d}:00", "%H:%M").time()

    def filter_rain_metric(self, start_time, end_time):
        """
        Generates an hourly list within a specified time period and extracts key rain metrics

        Each entry contains the following key-value pairs:
            - Time
            - chance of rain (percentage)
            - Expected precipitation amount (mm)

        :return: A time-sliced list of key rain metrics.
        """
        hourly_rain = []

        start_time_datetime = self.convert_to_datetime(start_time)
        end_time_datetime = self.convert_to_datetime(end_time)

        for each_hour in self.forecast_data["hour"]:
            time_datetime_conversion = datetime.strptime(each_hour["time"], "%Y-%m-%d %H:%M").time()

            # Only includes hours when rain is expected (API uses 1 = Yes)
            if ((start_time_datetime <= time_datetime_conversion <= end_time_datetime) and
                    each_hour["will_it_rain"] == 1):
                hourly_rain.append({
                    "time": time_datetime_conversion.strftime("%H:%M"),
                    "rain_percentage": each_hour["chance_of_rain"],
                    "rain_amount": each_hour["precip_mm"],
                })
        return hourly_rain

    def calculate_rain_coverage_percentage(self, rain_data):
        """
        Calculates the percentage of hours within a time period that have rain forecasted.

        :param rain_data: List of hourly rain data.

        :return: Integer percentage of hours with expected rain during the period.
        """
        return round(((len(rain_data)/self.duration)*100))

    def calculate_weighted_rain_probability(self, rain_data):
        """
        Calculates the average chance of rain across a time period

        :param rain_data: List of hourly rain data.

        :return: Integer percentage of average chance of rain
        """
        rain_percentage = 0
        for each_hour in rain_data:
            rain_percentage += each_hour["rain_percentage"]
        return round(rain_percentage/self.duration)

    def calculate_total_precipitation(self, rain_data):
        """
        Calculates the average chance of rain across a time period.

        :param rain_data: List of hourly rain data.

        :return: Integer representing the mean probability of rain.
        """
        total_precipitation = 0
        for each_hour in rain_data:
            total_precipitation += each_hour["rain_amount"]
        return round(total_precipitation, 2)

    def compile_during_window_rain_report(self):
        """
        Generates a formatted report summarizing rain conditions

        :return: A string containing the full report, structured with headers, metrics, and impact descriptions.
        """
        string_builder = StringIO()
        rain_data = self.filter_rain_metric(self.start_time, self.end_time)
        rain_status = self.rain_status(rain_data)
        string_builder.write(f"\n= = = 🌦️ RAIN 🌦️ = = =\n")
        if not rain_data:
            string_builder.write(f"{rain_status} RAIN (REPORT OMITTED)\n")
            return string_builder.getvalue()
        else:
            total_precipitation = self.calculate_total_precipitation(rain_data)
            rain_coverage_percentage = self.calculate_rain_coverage_percentage(rain_data)
            weighted_rain_probability = self.calculate_weighted_rain_probability(rain_data)
            weighted_rain_probability_result = self.weighted_rain_probability_impact(weighted_rain_probability)
            rain_coverage_result = self.rain_coverage_impact(rain_coverage_percentage)
            total_precipitation_result = self.total_precipitation_impact(total_precipitation)
            number_of_hour_of_rain = len(rain_data)

            string_builder.write(f"Rain {number_of_hour_of_rain}/{self.duration} hours | "
                                 f"Avg. Chance: {weighted_rain_probability}% | {total_precipitation} mm\n")
            string_builder.write(f"Probability: {weighted_rain_probability_result}\n"
                                 f"Coverage: {rain_coverage_result}\n"
                                 f"Precipitation: {total_precipitation_result}")
            string_builder.write(self.build_rain_timeline(rain_data))
        return string_builder.getvalue()

    def compile_pre_window_rain_report(self):
        """
        Generates a formatted report summarizing rain conditions

        :return: A string containing the full report, structured with headers, metrics, and impact descriptions.
        """
        string_builder = StringIO()
        rain_data = self.filter_rain_metric(self.pre_rain_window_start, self.start_time)
        total_precipitation = self.calculate_total_precipitation(rain_data)
        rain_status = self.rain_status(rain_data)

        string_builder.write(f"\n= = = 🌦️ PRIOR RAINFALL 🌦️ = = =\n")
        if not rain_data:
            string_builder.write(f"{rain_status} RAIN (REPORT OMITTED)\n")
        else:
            last_rain_hour = (rain_data[-1]["time"])
            impact = self.assess_pre_window_impact(last_rain_hour)
            string_builder.write(f"Rained {len(rain_data)}/{self.rain_check_hours_prior} "
                                 f"last hours (Last {last_rain_hour}) | "
                                 f"{total_precipitation} mm\n")
            string_builder.write(f"{impact}\n")
            string_builder.write(self.build_rain_timeline(rain_data))
        return string_builder.getvalue()

    def assess_pre_window_impact(self, last_rain_hour):
        """
        Assesses the last rainfall event and calculates the time difference (in hours) from the assigned start time,
        classifying it into one of three impact levels.

        :param last_rain_hour:  The last recorded hour of rainfall formatted in military time

        :return: A string describing the most recent rainfall before the assigned start time, including its impact level
        """
        last_hour_datetime_conversion = datetime.strptime(f"{last_rain_hour}", "%H:%M").time()
        
        datetime_difference = (datetime.combine(datetime.today(), self.convert_to_datetime(self.start_time)) -
                               datetime.combine(datetime.today(), last_hour_datetime_conversion))
        rain_time_difference_hours = datetime_difference.total_seconds() / 3600
        if rain_time_difference_hours >= self.LAST_HOUR_IMPACT_LOW:
            return "🟩 LOW (PLAYABLE)"
        elif rain_time_difference_hours >= self.LAST_HOUR_IMPACT_MODERATE:
            return "🟨 MODERATE (DELAY START)"
        else:
            return "🟥 HIGH (POSTPONE)"

    def rain_summary(self):
        """
        Generates a summary of impact levels for rainfall occurring both before and during the assessed time period

        :return: A formatted string describing the impact levels of precipitation prior to and  during the specified
        time window
        """
        string_builder = StringIO()
        string_builder.write(f"Rain Earlier: {self.rain_status(self.filter_rain_metric(self.pre_rain_window_start, 
                                                                                       self.start_time))}\n"
                             f"Rain Expected: {self.rain_status(self.filter_rain_metric(self.start_time,
                                                                                        self.end_time))}\n")
        return string_builder.getvalue()

    def rain_status(self, rain_data):
        """
        Assesses whether the array contains any rainfall data and returns the status as a string.

        :returns: 'Yes' if rain was detected, otherwise 'No'.
        """
        return "🟥 YES" if rain_data else "🟩 NO"

    def weighted_rain_probability_impact(self, weighted_rain_probability):
        """
        Classifies weighted rain probability into three impact levels

        :param weighted_rain_probability: The average chance of rain (%) during the assigned time period

        :return: A string describing the day's rain probability, including the impact level
        """
        if weighted_rain_probability <= self.RAIN_WEIGHTED_RAIN_PROBABILITY_LOW:
            return "🟩 LOW (PLAYABLE)"
        elif weighted_rain_probability <= self.RAIN_WEIGHTED_RAIN_PROBABILITY_MODERATE:
            return "🟨 MODERATE (CAUTION)\n"
        else:
            return "🟥 HIGH (UNPLAYABLE)\n"

    def rain_coverage_impact(self, rain_coverage):
        """
        Classifies the percentage of total hours with rain into three impact levels

        :param rain_coverage: The percentage of total hours with rain forecasted

        :return: A string describing the day's rain coverage, including the impact level
        """
        if rain_coverage <= self.RAIN_COVERAGE_LOW:
            return "🟩 LOW (PLAYABLE)"
        elif rain_coverage <= self.RAIN_COVERAGE_MODERATE:
            return "🟨 MODERATE (CAUTION)\n"
        else:
            return "🟥 HIGH (UNPLAYABLE)\n"

    def total_precipitation_impact(self, total_precipitation):
        """
        Classifies precipitation levels into three impact categories and generates an hourly timeline
        of rainfall amounts

        :param total_precipitation: An integer representing the maximum precipitation (mm) in the forecast data

        :return: A string describing the day's rainfall conditions, including the impact level classification
        """
        if total_precipitation <= self.RAIN_PRECIPITATION_LOW:
            return f"🟩 LOW (VERY LIGHT RAIN)\n"
        elif total_precipitation <= self.RAIN_PRECIPITATION_MODERATE:
            return "🟨 MODERATE (LIGHT RAIN)\n"
        else:
            return "🟥 HIGH (HEAVY RAIN)\n"

    def build_rain_timeline(self, rain_data):
        """
        Generates hourly temperature forecast data formatted as a chronological timeline.

        Each entry includes:
        - Time (in `HH:MM` format)
        - Chance of Rain (%) or expected amount of total precipitation (mm)

        :return: None
        """
        string_builder = StringIO()
        string_builder.write(f"- - - TOP {self.top_timeline_count} PEAK RAIN HOURS - - -\n")
        sort_by_max = sorted(rain_data, key=lambda item: item["rain_percentage"], reverse=True)[
                      :self.top_timeline_count]
        sort_by_time = sorted(sort_by_max, key=lambda item: item["time"])
        for each_hour in sort_by_time:
            string_builder.write(f"\t{each_hour['time']}: {each_hour['rain_percentage']}% "
                                 f"({each_hour['rain_amount']} mm)\n")
        return string_builder.getvalue()
