from io import StringIO
from datetime import datetime


class Alert:
    """
    Designed to manage and send weather alerts and warnings based on geographical location
    """
    def __init__(self, forecast_alert_data):
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
        if self.forecast_alert_data:
            last_weather_alert_index = self.forecast_alert_data[-1]
            return {"headline": last_weather_alert_index["headline"], "msgtype": last_weather_alert_index["msgtype"],
                    "severity": last_weather_alert_index["severity"], "event": last_weather_alert_index["event"],
                    "urgency": last_weather_alert_index["urgency"],
                    "effective": datetime.strptime(last_weather_alert_index["effective"],
                                                   "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d (%H:%M)"),
                    "expires": datetime.strptime(last_weather_alert_index["expires"],
                                                 "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d (%H:%M)")
                    }
        else:
            return None

    def alert_summary(self):
        """
        Generates a summary of any active weather alerts or warnings

        :return: A formatted string describing the status of weather alerts for the forecast period
        """
        string_builder = StringIO()
        alert_data = self.filter_alert_metrics()
        string_builder.write(f"Alert: {self.alert_status(alert_data)}\n")
        return string_builder.getvalue()

    def alert_status(self, alert_data):
        """
        Assesses whether the array contains any alert data and returns the status as a string

        :returns: 'ACTIVE' and its severity if an alert is detected, otherwise 'NOT ACTIVE'
        """
        return f"🟩 NOT ACTIVE" if not alert_data else f"🟩 ACTIVE ({alert_data['severity'].upper()})"

    def alert_report(self):
        """
        Generates a formatted summary of active weather alerts and warnings

        :return: A structured string report containing headers, status, and detailed information
        """
        alert_data = self.filter_alert_metrics()
        string_builder = StringIO()
        alert_status = self.alert_status(alert_data)
        string_builder.write(f"\n= = = ⚠️ ALERT ⚠️ = = =\n")
        if alert_data:
            string_builder.write(f"{alert_data['effective']} - {alert_data['expires']}\n"
                                 f"{alert_status}\n"
                                 f"Hazard: {alert_data['event'].upper()}\n"
                                 f"Note: {alert_data['headline'].upper()}\n")
        else:
            string_builder.write(f"{alert_status} (REPORT OMITTED)\n")
        return string_builder.getvalue()
