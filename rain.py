from io import StringIO
from datetime import datetime
class Rain:
    """
    A class to filter, analyze, and report rain-related weather data.
    """
    def __init__(self,weather_data,START_TIME, END_TIME, TOP_TIMELINE_COUNT, RAIN_CHECK_HOURS_PRIOR):
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
        timeline = []
        format_start_time = datetime.strptime(f"{START_TIME:02d}:00", "%H:%M").time()
        format_end_time = datetime.strptime(f"{END_TIME:02d}:00", "%H:%M").time()

        for each_hour in hourly:
            format_time =  datetime.strptime(each_hour["time"],"%Y-%m-%d %H:%M").time()

            # Only includes hours where rain is expected (API uses 1 = Yes)
            if (format_time>= format_start_time and format_time <=format_end_time) and each_hour["will_it_rain"] ==1:
                timeline.append({
                    "time": format_time.strftime("%H:%M"),
                    "rain_percentage":each_hour["chance_of_rain"],
                    "rain_amount":each_hour["precip_mm"],
                })
        if (timeline):
            for each_key in list(timeline[0].keys())[1:]:
                self.METRIC_LIST.append(each_key)
        return timeline

    def calculate_rain_percentage(self, time_period_forecast):
        """
        Calculates the probability of rain occurring during a given time period.

        :param time_period_forecast: List of rain data by time slice.

        :return: String containing the day's rain status, including impact level description when applicable.
        """
        total=1
        for each_rain_percentage in time_period_forecast:
            total*=(1-(each_rain_percentage["rain_percentage"]/100))
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

    def compile_during_window_rain_report(self):
        """
        Generates a formatted report summarizing rain conditions

        :return: A string containing the full report, structured with headers, metrics, and impact descriptions.
        """
        string_builder=StringIO()
        time_period_forecast=self.filter_rain_metric(self.START_TIME,self.END_TIME)
        string_builder.write("\n= = = RAIN REPORT = = =\n")
        string_builder.write(f"Is rain expected: ")
        if not time_period_forecast:
            string_builder.write(f"NO\n"
                                 f"REPORT OMITTED\n")
        else:
            total_precipitation = self.calculate_total_precipitation(time_period_forecast)
            total_chance_of_rain = self.calculate_rain_percentage(time_period_forecast)
            string_builder.write(f"YES\n")
            impact = {"rain_percentage": self.chance_of_rain_impact(total_chance_of_rain),
                      "rain_amount": self.total_precipitation_impact(total_chance_of_rain)
                      }
            value = {
                "rain_percentage": f"{total_chance_of_rain}% over {self.END_TIME - self.START_TIME} hours",
                "rain_amount": f"{total_precipitation}mm"
            }
            for metric in self.METRIC_LIST:
                display_metric_title = metric.replace("_", " ")

                string_builder.write(f"- - - {display_metric_title.upper()} - - - \n"
                                         f"{display_metric_title.title()}: {value[metric]}\n")
                string_builder.write(f"Impact: {impact[metric]}\n")
                string_builder.write(self.build_rain_timeline(time_period_forecast,metric))
        return string_builder.getvalue()


    def compile_pre_window_rain_report(self):
        """
        Generates a formatted report summarizing rain conditions

        :return: A string containing the full report, structured with headers, metrics, and impact descriptions.
        """
        string_builder=StringIO()
        time_period_forecast = self.filter_rain_metric((self.START_TIME-self.RAIN_CHECK_HOURS_PRIOR),self.START_TIME+1)
        string_builder.write("\n= = = PRE-RAIN REPORT = = =\n")
        string_builder.write(f"Was there precipitation {self.RAIN_CHECK_HOURS_PRIOR} hours prior to start time ({self.START_TIME}:00)?: ")
        if not (time_period_forecast):
            string_builder.write(f"NO\n"
                                 f"REPORT OMITTED\n")
        else:
            string_builder.write(f"YES\n")
            string_builder.write(f"Rained A Total of {len(time_period_forecast)} hours out of {self.RAIN_CHECK_HOURS_PRIOR} hours ({self.calculate_total_precipitation(time_period_forecast)}mm)\n")
            string_builder.write(f"Last rainfall: {(time_period_forecast[0]["time"])[:-1]}")
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

    def build_rain_timeline(self, time_period_forecast, metric):
        """
        Generates hourly temperature forecast data formatted as a chronological timeline.

        Each entry includes:
        - Time (in `HH:MM` format)
        - Chance of Rain (%) or expected amount of total precipitation (mm)

        :return: None
        """
        string_builder=StringIO()
        display_metric_name = metric.replace("_", " ")
        string_builder.write(f"- - - TOP {self.TOP_TIMELINE_COUNT} PEAK {display_metric_name.upper()} HOURS - - -\n")
        sort_by_max = sorted(time_period_forecast, key=lambda item: item[f"{metric}"], reverse=True)[
                      :self.TOP_TIMELINE_COUNT]
        sort_by_time = sorted(sort_by_max, key=lambda item: item["time"])
        for each_hour in sort_by_time:
            if (metric == "rain_percentage"):
                string_builder.write(f"\t{each_hour["time"]}: {each_hour[f"{metric}"]} % \n")
            else:
                string_builder.write(f"\t{each_hour["time"]}: {each_hour[f"{metric}"]} mm\n")
        return string_builder.getvalue()







