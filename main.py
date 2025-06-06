import requests
from dotenv import load_dotenv
import os

FORECAST_DAYS = 3 #Number of days to forecast
load_dotenv()

parameters={
    "q": f"{os.getenv("LAT")},{os.getenv("LON")}",
    "key": os.getenv("API_KEY"),
    "days": FORECAST_DAYS
}

# TODO: Implement main() and response() functions
weatherResponse = requests.get(os.getenv("URL"), params=parameters)
weatherData = weatherResponse.json()



