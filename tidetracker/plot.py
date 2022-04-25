
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pytz

from tidetracker import config


# Plot last 12 hours and next 12 hours
def tide(heights, show=False):
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

    timezone = pytz.timezone(config.TIME_ZONE)
    major_date_formatter = mdates.DateFormatter("%a", tz=timezone)
    minor_date_formatter = mdates.DateFormatter("%-H", tz=timezone)
    axs.xaxis.set_major_formatter(major_date_formatter)
    axs.xaxis.set_minor_formatter(minor_date_formatter)
    axs.xaxis.label.set_visible(False)
    axs.fill_between(
        heights["datetime"], heights["height"], heights["height"].min(), color="black"
    )
    if show:
        plt.show()
    plt.savefig("images/TideLevel.png", dpi=60)
