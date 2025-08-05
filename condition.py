from statistics import mode
class Condition:
    """
    A class that processes weather data, evaluates the condition and generates a report.
    """
    def __init__(self,weather_data, START_TIME, END_TIME,TOP_TIMELINE_COUNT,DAYS_TO_SHOW):
        self.weather_data = weather_data
        self.START_TIME = START_TIME
        self.END_TIME = END_TIME
        self.TOP_TIMELINE_COUNT = TOP_TIMELINE_COUNT
        self.METRIC_LIST = []
        self.DAYS_TO_SHOW = DAYS_TO_SHOW

    def filter_condition_metrics(self):
        """
        Generates an hourly list within a specified time period and extracts weather condition texts and codes.

        Conditions can include: Sunny, Mist, Overcast, etc.

        :return: A time-sliced list containing hourly condition texts and codes.
        """
        hourly = self.weather_data["forecast"]["forecastday"][self.DAYS_TO_SHOW]["hour"]
        timeline = [
            {"condition_text": each_hour["condition"]["text"], "condition_code": each_hour["condition"]["code"]} for each_hour in hourly
        ]
        self.METRIC_LIST = list(timeline[0].keys())[1:]
        return (timeline[self.START_TIME:self.END_TIME])

    def find_condition_mode(self):
        """
        Finds the most frequently appeared condition value

        :return:  The most common condition value observed during the specified period
        """
        time_period_forecast = self.filter_condition_metrics()
        condition_list= [each_hour["condition_text"] for each_hour in time_period_forecast]
        most_common_condition= mode(condition_list)
        return (most_common_condition)

    def condition_summary(self):
        """
        Summarizes and displays the overall condition for the specified time period

        :return: A formatted string representing the condition
        """
        return f"Condition: {self.find_condition_mode()}\n"









