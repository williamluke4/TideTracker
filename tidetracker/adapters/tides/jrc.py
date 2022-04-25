import arrow
import pandas as pd
import requests
from scipy import signal  # filtering etc.
from tidetracker import config, plot

JRC_URL = "https://webcritech.jrc.ec.europa.eu/SeaLevelsDb/api/Device/"
DEVICE_ID = "940"
TIME_ZONE = "Africa/Nairobi"


def get_peaks_and_troughs(tide_df):
    peaks, _ = signal.find_peaks(tide_df["height"])
    troughs, _ = signal.find_peaks(-tide_df["height"])

    peaks_troughs = []
    for peak in peaks:
        peaks_troughs.append(
            {
                "datetime": tide_df.iloc[peak]["datetime"],
                "height": tide_df.iloc[peak]["height"],
                "state": "HIGH TIDE",
            }
        )
    for trough in troughs:
        peaks_troughs.append(
            {
                "datetime": tide_df.iloc[trough]["datetime"],
                "height": tide_df.iloc[trough]["height"],
                "state": "LOW TIDE",
            }
        )

    peaks_troughs_df = pd.DataFrame(
        peaks_troughs, columns=["datetime", "height", "state"]
    )
    peaks_troughs_df.index = peaks_troughs_df["datetime"]
    return peaks_troughs_df


def get():
    from_time = arrow.utcnow().shift(hours=-12).format("YYYY-MM-DD HH:mm:ss")
    to_time = arrow.utcnow().shift(hours=12).format("YYYY-MM-DD HH:mm:ss")
    querystring = {
        "tMin": from_time,
        "tMax": to_time,
        "nPts": "300",
        "field": "tide",
    }
    headers = {
        "referrer": "https://webcritech.jrc.ec.europa.eu/SeaLevelsDb/Tools/Chart/?deviceId=940",
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "x-requested-with": "XMLHttpRequest",
    }
    response = requests.request(
        "GET",
        f"{JRC_URL}{DEVICE_ID}/Data",
        params=querystring,
        headers=headers,
    )
    data = response.json()
    tide_df = pd.DataFrame(data, columns=["Date", "Value"])
    tide_df.rename(columns={"Date": "datetime", "Value": "height"}, inplace=True)
    tide_df["datetime"] = pd.to_datetime(tide_df["datetime"]).dt.tz_convert(
        config.TIME_ZONE
    )
    tide_df["datetime"] = tide_df["datetime"]
    tide_df.index = tide_df["datetime"]

    peaks_troughs_df = get_peaks_and_troughs(tide_df)

    return peaks_troughs_df, tide_df


# https://webcritech.jrc.ec.europa.eu/SeaLevelsDb/api/Device/940/Data?tMin=2022-04-22%2006%3A18%3A39&tMax=2022-04-26%2006%3A18%3A39&nPts=3000&field=ss
if __name__ == "__main__":
    peaksAndTroughsDF, tideDF = get()
    plot.tide(tideDF, show=True)
    print(peaksAndTroughsDF)
