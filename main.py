import requests
from dotenv import load_dotenv
import os

# Number of days to forecast
FORECAST_DAYS = 3

# TODO: Create Try Except
def retrieveAPIResponse():
    weatherResponse = requests.get(os.getenv("URL"), params= {"q": f"{os.getenv("LAT")},{os.getenv("LON")}",
                                                              "key": os.getenv("API_KEY"), "days": FORECAST_DAYS})
    return weatherResponse.json()
def main():
    load_dotenv()
    weatherData = retrieveAPIResponse()

main()



