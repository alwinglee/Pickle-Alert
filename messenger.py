import os
from twilio.rest import Client
class Messenger:
    def __init__(self, report_details,date_details):
        self.report_details = report_details
        self.date_details = date_details
        self.send_message()

    def send_message(self):
        """
        Sends the weather forecast report as a message using Twilio

        :return: A formatted string detailing the forecasted day's weather, including its generation date and report count
        """
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)
        report = self.report_details.format_report()
        page_total = len(report)
        page_count = 1

        for key, value in report.items():
            client.messages.create(
                body=f"[{self.date_details.display_forecast_date()} | Msg. {page_count}/{page_total}]\n"
                     f"[{self.date_details.display_report_date()}]\n"
                     f"{value}\n",
                from_=os.getenv("PHONE_NUMBER"),
                to=os.getenv("MY_PHONE_NUMBER"),
            )
            page_count += 1
