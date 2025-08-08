from statistics import mode
class Condition:
    """
    A class that processes weather data, evaluates the condition and generates a report.
    """
    def __init__(self,hourly_selected_forecast_data):
        self.hourly_selected_forecast_data = hourly_selected_forecast_data

    def filter_condition_metrics(self):
        """
        Generates an hourly list within a specified time period and extracts weather condition texts and codes.

        Conditions can include: Sunny, Mist, Overcast, etc.

        :return: A time-sliced list containing hourly condition texts and codes.
        """
        timeline = [
            {"condition_text": each_hour["condition"]["text"], "condition_code": each_hour["condition"]["code"]}
            for each_hour in self.hourly_selected_forecast_data]
        return timeline

    def find_condition_mode(self):
        """
        Finds the most frequently appeared condition value

        :return:  The most common condition value observed during the specified period
        """
        time_period_forecast = self.filter_condition_metrics()
        condition_list= [each_hour["condition_text"] for each_hour in time_period_forecast]
        dominant_condition= mode(condition_list)
        return (dominant_condition)

    def condition_summary(self):
        """
        Summarizes and displays the overall condition for the specified time period

        :return: A formatted string representing the condition
        """
        return f"Condition: {self.find_condition_mode()}\n"









