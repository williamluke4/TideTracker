from datetime import datetime, date, timedelta



import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import requests
from tidetracker import config


# Get High and Low tide info for today
def get_tide_extremes():
    start_today = datetime.combine(date.today(), datetime.min.time())
    duration = 24 * 60  # 1 day in mins
    querystring = {
        "longitude": config.LONGITUDE,
        "latitude": config.LATITUDE,
        "interval": "60",
        "duration": duration,
        "timestamp": int(start_today.timestamp()),
    }

    response = requests.request(
        "GET",
        config.RAPIDAPI_URL,
        headers=config.RAPIDAPI_HEADERS,
        params=querystring,
    )
    data = response.json()

    extremes = data.get("extremes")
    extremesDF = pd.DataFrame(
        extremes, columns=["timestamp", "datetime", "height", "state"]
    )
    extremesDF["datetime"] = pd.to_datetime(extremesDF["datetime"])
    extremesDF.index = extremesDF["datetime"]

    return extremesDF


# Plot last 12 hours and next 12 hours
def plot_tide(heights):
    # Create Plot
    _fig, axs = plt.subplots(figsize=(12, 4))
    heights["height"].plot.line(ax=axs, color="none")
    plt.title("Tides", fontsize=20)
    # fontweight="bold",
    # axs.xaxis.set_tick_params(labelsize=20)
    # axs.yaxis.set_tick_params(labelsize=20)

    for pos in ["right", "top", "bottom", "left"]:
        plt.gca().spines[pos].set_visible(False)

    axs.xaxis.set_major_locator(mdates.DayLocator())
    axs.xaxis.set_minor_locator(mdates.HourLocator())

    major_date_formatter = mdates.DateFormatter("%a")
    minor_date_formatter = mdates.DateFormatter("%-H")
    axs.xaxis.set_major_formatter(major_date_formatter)
    axs.xaxis.set_minor_formatter(minor_date_formatter)
    axs.xaxis.label.set_visible(False)
    axs.fill_between(
        heights["datetime"], heights["height"], heights["height"].min(), color="black"
    )
    plt.savefig("images/TideLevel.png", dpi=60)
    # plt.show()


def get_tide_data_for_plot():
    today = datetime.now()
    yesterday = today - timedelta(days=0.5)
    interval = 30
    duration = 24 * 60  # mins from timestamp
    querystring = {
        "longitude": config.LONGITUDE,
        "latitude": config.LATITUDE,
        "interval": interval,
        "duration": duration,
        "timestamp": int(yesterday.timestamp()),
    }

    response = requests.request(
        "GET",
        config.RAPIDAPI_URL,
        headers=config.RAPIDAPI_HEADERS,
        params=querystring,
    )
    data = response.json()
    print(data)
    heights = data["heights"]
    heightsDF = pd.DataFrame(
        heights, columns=["timestamp", "datetime", "height", "state"]
    )

    heightsDF["datetime"] = pd.to_datetime(heightsDF["datetime"])
    # TODO: Use device tz
    heightsDF["datetime"] = heightsDF["datetime"] + pd.Timedelta(
        "03:00:00"
    )  # Change TZ from utc to utc+3
    heightsDF.index = heightsDF["datetime"]
    return heightsDF


if __name__ == "__main__":
    tides = get_tide_data_for_plot()
    plot_tide(tides)


