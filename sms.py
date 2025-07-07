import os
from twilio.rest import Client
class Twilio:
    def __init__(self,report_details):
        self.report_details=report_details
        self.send_message()


    def send_message(self):
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        client = Client(account_sid, auth_token)

        client.messages.create(
            body=self.report_details,
            from_=os.environ["PHONE_NUMBER"],
            to=os.environ["MY_PHONE_NUMBER"],
        )


