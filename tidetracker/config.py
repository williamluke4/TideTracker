from decouple import config
import os
# Optional, displayed on top left
LOCATION = config("LOCATION", default="Kilifi Kenya")

LATITUDE = config("LATITUDE", default="-3.67275")
LONGITUDE = config("LONGITUDE", default="39.87769")

UNITS = config("UNITS", default="metric")

# For weather data
# Create Account on openweathermap.com and get API key
OPENWEATHERMAP_API_KEY = config("OPENWEATHERMAP_API_KEY")

# RapidAPI Tides
# Create Account on rapidapi.com, subscribe to :down: and get an API key
# Docs: https://rapidapi.com/apihood/api/tides/
RAPID_API_KEY = config("RAPID_API_KEY")

#  Time between refreshing the screen and data
REFRESH_INTERVAL = config("REFRESH_INTERVAL", default=10, cast=int)  # mins

# Open Weathermap API URL
BASE_URL = "http://api.openweathermap.org/data/2.5/onecall?"
OPENWEATHERMAP_URL = (
    BASE_URL
    + "lat="
    + LATITUDE
    + "&lon="
    + LONGITUDE
    + "&units="
    + UNITS
    + "&appid="
    + OPENWEATHERMAP_API_KEY
)


RAPIDAPI_URL = "https://tides.p.rapidapi.com/tides"
RAPIDAPI_HEADERS = {
    "X-RapidAPI-Host": "tides.p.rapidapi.com",
    "X-RapidAPI-Key": RAPID_API_KEY,
}


PIC_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "images")
ICON_DIR = os.path.join(PIC_DIR, "icon")
FONT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "font")
