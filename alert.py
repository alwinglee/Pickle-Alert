from io import StringIO
from datetime import datetime
class Alert:
    def __init__(self,forecast_alert_data):
        self.forecast_alert_data = forecast_alert_data

    def filter_alert_metrics(self):
        """
        Retrieves the latest weather alert from the specified geographical location

        Each entry contains the following key-value pairs:
            - headline
            - msgtype
            - severity
            - event
            - urgency
            - effective
            - expires

        :return: List containing the latest weather alert data
        """

        if (self.forecast_alert_data):
            last_weather_alert_index = self.forecast_alert_data[-1]
            return  {"headline":last_weather_alert_index ["headline"],"msgtype":last_weather_alert_index ["msgtype"],
                     "severity":last_weather_alert_index ["severity"],"event":last_weather_alert_index ["event"],
                     "urgency":last_weather_alert_index ["urgency"],
                     "effective": datetime.strptime(last_weather_alert_index ["effective"],("%Y-%m-%dT%H:%M:%S%z")).strftime("%Y-%m-%d (%H:%M)") ,
                     "expires":datetime.strptime(last_weather_alert_index ["expires"],("%Y-%m-%dT%H:%M:%S%z")).strftime("%Y-%m-%d (%H:%M)")
            }
        else:
            return None

    def alert_summary(self):
        string_builder = StringIO()
        time_period_forecast = self.filter_alert_metrics()
        string_builder.write(f"Alert: {self.alert_status(time_period_forecast)}\n")
        return string_builder.getvalue()

    def alert_status(self,time_period_forecast):
        return f"🟩 NOT ACTIVE" if not (time_period_forecast) else f"🟩 ACTIVE({time_period_forecast["severity"].upper()})"

    def alert_report(self):
        time_period_forecast = self.filter_alert_metrics()
        string_builder = StringIO()
        alert_status= self.alert_status(time_period_forecast)
        string_builder.write(f"\n= = = ⚠️ ALERT ⚠️ = = =\n")
        if time_period_forecast:
            string_builder.write(f"{time_period_forecast["effective"]} - {time_period_forecast["expires"]}\n"
                                 f"{alert_status}\n"
                                 f"- - - {time_period_forecast["event"].upper()} - - -\n"
                                 f"{time_period_forecast["headline"].title()}\n")
        else:
            string_builder.write(f"{alert_status} (REPORT OMITTED)\n")
        return string_builder.getvalue()

