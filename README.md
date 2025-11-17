Title: Pickle-Alert

Table of Contents:
- Introduction
- Installation
- Dependencies
- Required File
- Features
- Project Status
- Used Technologies
- Author's Information

Introduction:
- Pickle-Alert is a script that sends daily weather forecasts to your personal device. It helps pickleball players determine the best times to play by providing clear indicators for conditions like wind and rain.

Installation:
- No installation is required to use the Python script files directly.

Dependencies:
- Requires a user's phone number to receive daily text messages.
- Weather forecast data is retrieved from WeatherAPI.com. Connection errors to their servers will disrupt the script.
- Twilio is used as the communication platform. Messages will not be sent if their servers experience technical difficulties.

Required File:
- All files are essential, especially main.py, which controls the configuration of the daily weather forecast text messages.

Features:
- Display Key Metrics: Shows metrics that may affect a pickleball session, including rain (before and during), wind speed, wind gust, "feels like" temperature, and humidity. Values are presented for each hour within the set start and end time.
- Alert Section: Provides weather alerts that may impact your pickleball plans in addition to the standard forecast.
- Summary Section: Offers a visual (emoji) and brief summary indicating the overall weather forecast for the day.
- Rainfall Section: Notifies users of rainfall before and during the selected timeframe.
- Error Handling: Validates user inputs to ensure the script runs properly.

Project Status:
- Status: Ongoing
- Known Limitations:
    - The WeatherAPI.com API cannot detect spontaneous, last-minute changes such as brief downpours.
    - Twilio may send messages out of order.

Used Technologies:
- Twilio: A communication platform that provides developers with tools to communicate with users via email, voice, and SMS.
- WeatherAPI.com: Provides weather forecast data.
- Language: Python 3.12
- Modules:
    - io (StringIO)
    - datetime (datetime)
    - os
    - requests
    - twilio.rest (Client)
    - statistics (mode)

Author's Information:
- Created by Alwin Lee
- Contact: alwin.lee@mohawkcollege.ca

