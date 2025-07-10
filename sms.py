# import os
# from twilio.rest import Client
# class Sms:
#     def __init__(self, report_details):
#         self.report = report_details  # This is the Report object
#         self.send_message()
#
#     def send_message(self):
#
#         account_sid = os.getenv("TWILIO_ACCOUNT_SID")
#         auth_token = os.getenv("TWILIO_AUTH_TOKEN")
#         client = Client(account_sid, auth_token)
#
#         client.messages.create(
#             body=self.report.format_report(),
#             from_=os.getenv("PHONE_NUMBER"),
#             to=os.getenv("MY_PHONE_NUMBER"),
#         )
#
#
#
#
#
