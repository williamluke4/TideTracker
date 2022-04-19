import json

import requests

from tidetracker import config
from tidetracker.screen import Screen


# define function for getting weather data
def get_weather(screen: Screen):
    # Ensure there are no errors with connection
    error_connect = True
    while error_connect == True:
        try:
            # HTTP request
            print("Attempting to connect to OWM.")
            response = requests.get(config.OPENWEATHERMAP_URL)
            print("Connection to OWM successful.")
            error_connect = None
        except:
            # Call function to display connection error
            print("Connection error.")
            screen.display_error("CONNECTION")

    # Check status of code request
    if response.status_code == 200:
        print("Connection to Open Weather successful.")
        # get data in jason format
        data = response.json()

        with open("data.txt", "w") as outfile:
            json.dump(data, outfile)

        return data

    else:
        # Call function to display HTTP error
        screen.display_error("HTTP")
