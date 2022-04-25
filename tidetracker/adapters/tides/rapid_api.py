from datetime import date, datetime, timedelta

import pandas as pd
import requests
from tidetracker import config, plot


# Get High and Low tide info for today
def get_peaks_and_troughs():
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

    peaks_troughs = data.get("extremes")
    peaks_troughs_df = pd.DataFrame(
        peaks_troughs, columns=["datetime", "height", "state"]
    )
    peaks_troughs_df["datetime"] = pd.to_datetime(
        peaks_troughs_df["datetime"]).dt.tz_convert(config.TIME_ZONE)
    peaks_troughs_df.index = peaks_troughs_df["datetime"]

    return peaks_troughs_df


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
    heights = data["heights"]
    tide_df = pd.DataFrame(
        heights, columns=["datetime", "height"]
    )

    tide_df["datetime"] = pd.to_datetime(
        tide_df["datetime"]).dt.tz_convert(config.TIME_ZONE)
    tide_df.index = tide_df["datetime"]
    return tide_df


def get():
    tide_df = get_tide_data_for_plot()
    peaks_troughs_df = get_peaks_and_troughs()
    return peaks_troughs_df, tide_df


if __name__ == "__main__":
    peaksAndTroughsDF, tideDF = get()
    plot.tide(tideDF)
    print(peaksAndTroughsDF)
