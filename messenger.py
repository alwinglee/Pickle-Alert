import os
from twilio.rest import Client


class Messenger:
    """
    Connects to the Twilio API to send weather forecast reports to an authorized phone number
    """
    # The limit is 1024; however, it was reduced account for forecast and generation date details
    TWILIO_WHATSAPP_CHARACTER_LIMIT = 950

    def __init__(self, report_details, date_details):
        self.report_content = report_details.formatted_report
        self.date_details = date_details
        self.send_message()

    def split_report(self):
        """
        Takes the content of the final report and splits it into individual messages to avoid exceeding the
        character limit

        :return: List of segmented parts of the report
        """
        report_segments = []
        content = self.report_content

        if not content:
            return report_segments
        if len(content) <= self.TWILIO_WHATSAPP_CHARACTER_LIMIT:
            report_segments.append(content)
            return report_segments

        while content and len(content) > 0:
            current_segment = content[:self.TWILIO_WHATSAPP_CHARACTER_LIMIT]
            new_line_index = current_segment.rfind("\n")
            if new_line_index == -1:
                report_segments.append(current_segment)
                content = content[self.TWILIO_WHATSAPP_CHARACTER_LIMIT:]
            else:
                report_segments.append(content[:new_line_index + 1])
                content = content[new_line_index + 1:]
        return report_segments

    def send_message(self):
        """
        Sends the weather forecast report as a message using Twilio

        :return: A formatted string detailing the forecasted day's weather, including its generation date and
         report count
        """
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)

        for each_segment in self.split_report():
            client.messages.create(
                body=f"{each_segment}\n",
                from_=os.getenv("PHONE_NUMBER"),
                to=os.getenv("MY_PHONE_NUMBER"),
            )
