from statistics import mode


class Condition:
    """
    A class that processes weather data, evaluates the condition and generates a report
    """
    def __init__(self, hourly_selected_forecast_data):
        self.hourly_selected_forecast_data = hourly_selected_forecast_data

    def filter_condition_metrics(self):
        """
        Generates an hourly list within a specified time period and extracts weather condition texts and codes

        Conditions can include: Sunny, Mist, Overcast, etc

        :return: A time-sliced list containing hourly condition texts and codes
        """
        return [{"condition_text": each_hour["condition"]["text"], "condition_code": each_hour["condition"]["code"]}
                for each_hour in self.hourly_selected_forecast_data]

    def find_condition_mode(self):
        """
        Finds the most frequently appeared condition value

        :return: The most common condition value observed during the specified period
        """
        condition_data = self.filter_condition_metrics()
        condition_list = [each_hour["condition_text"] for each_hour in condition_data]
        return mode(condition_list)

    def condition_summary(self):
        """
        Summarizes and displays the overall condition for the specified time period

        :return: A formatted string representing the condition
        """
        return f"Condition: {self.find_condition_mode()}\n"
