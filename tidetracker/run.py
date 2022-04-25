#!/usr/bin/python3

import datetime as dt
import logging
import os

from PIL import Image, ImageDraw

from tidetracker import adapters, config, plot, style
from tidetracker import weather as weath
from tidetracker.screen import Screen

log = logging.getLogger(__name__)


def main():
    screen = Screen()

    while True:
        # Get weather data
        data = weath.get_weather(screen)

        # get current dict block
        current = data["current"]
        # get current
        temp_current = current["temp"]
        # get feels like
        feels_like = current["feels_like"]
        # get humidity
        # humidity = current["humidity"]
        # get pressure
        wind = current["wind_speed"]
        # get description
        weather = current["weather"]
        report = weather[0]["description"]
        # get icon url
        icon_code = weather[0]["icon"]

        # get daily dict block
        daily = data["daily"]
        # get daily precip
        daily_precip_float = daily[0]["pop"]
        # format daily precip
        daily_precip_percent = daily_precip_float * 100
        # get min and max temp
        daily_temp = daily[0]["temp"]
        temp_max = daily_temp["max"]
        temp_min = daily_temp["min"]

        # Set strings to be printed to screen
        # string_location = config.LOCATION
        string_temp_current = format(temp_current, ".0f") + "\N{DEGREE SIGN}C"
        string_feels_like = "Feels like: " + \
            format(feels_like, ".0f") + "\N{DEGREE SIGN}C"
        # string_humidity = "Humidity: " + str(humidity) + "%"
        string_wind = "Wind: " + format(wind, ".1f") + " KPH"
        string_report = "Now: " + report.title()
        string_temp_max = "High: " + \
            format(temp_max, ">.0f") + "\N{DEGREE SIGN}C"
        string_temp_min = "Low:  " + \
            format(temp_min, ">.0f") + "\N{DEGREE SIGN}C"
        string_precip_percent = "Precip: " + \
            str(format(daily_precip_percent, ".0f")) + "%"

        # get min and max temp
        nx_daily_temp = daily[1]["temp"]
        nx_temp_max = nx_daily_temp["max"]
        nx_temp_min = nx_daily_temp["min"]
        # get daily precip
        nx_daily_precip_float = daily[1]["pop"]
        # format daily precip
        nx_daily_precip_percent = nx_daily_precip_float * 100

        # get min and max temp
        nx_nx_daily_temp = daily[2]["temp"]
        nx_nx_temp_max = nx_nx_daily_temp["max"]
        nx_nx_temp_min = nx_nx_daily_temp["min"]
        # get daily precip
        nx_nx_daily_precip_float = daily[2]["pop"]
        # format daily precip
        nx_nx_daily_precip_percent = nx_nx_daily_precip_float * 100

        # Tomorrow Forcast Strings
        nx_day_high = "High: " + \
            format(nx_temp_max, ">.0f") + "\N{DEGREE SIGN}C"
        nx_day_low = "Low: " + format(nx_temp_min, ">.0f") + "\N{DEGREE SIGN}C"
        nx_precip_percent = "Precip: " + \
            str(format(nx_daily_precip_percent, ".0f")) + "%"
        nx_weather_icon = daily[1]["weather"]
        nx_icon = nx_weather_icon[0]["icon"]

        # Overmorrow Forcast Strings
        nx_nx_day_high = "High: " + \
            format(nx_nx_temp_max, ">.0f") + "\N{DEGREE SIGN}C"
        nx_nx_day_low = "Low: " + \
            format(nx_nx_temp_min, ">.0f") + "\N{DEGREE SIGN}C"
        nx_nx_precip_percent = (
            "Precip: " + str(format(nx_nx_daily_precip_percent, ".0f")) + "%"
        )
        nx_nx_weather_icon = daily[2]["weather"]
        nx_nx_icon = nx_nx_weather_icon[0]["icon"]

        # Last updated time
        now = dt.datetime.now()
        current_time = now.strftime("%H:%M")
        last_update_string = "Last Updated: " + current_time

        # Tide Data
        # Get water level
        wl_error = True
        while wl_error is True:
            try:
                peaks_troughs_df, tide_df = adapters.tides.jrc.get()
                wl_error = False
            except Exception as e:
                screen.display_error("Tide Data")
                log.error(e)

        plot.tide(tide_df)

        # Open template file
        template = Image.open(os.path.join(config.PIC_DIR, "template.png"))
        # Initialize the drawing context with template as background
        draw = ImageDraw.Draw(template)

        # Current weather
        # Open icon file
        icon_file = icon_code + ".png"
        icon_image = Image.open(os.path.join(config.ICON_DIR, icon_file))
        icon_image = icon_image.resize((130, 130))
        template.paste(icon_image, (50, 50))

        draw.text((125, 10), config.LOCATION,
                  font=style.FONT_35, fill=style.BLACK)

        # Center current weather report
        w, h = draw.textsize(string_report, font=style.FONT_20)
        # print(w)
        if w > 250:
            string_report = "Now:\n" + report.title()

        center = int(120 - (w / 2))
        draw.text((center, 175), string_report,
                  font=style.FONT_20, fill=style.BLACK)

        # Data
        draw.text((250, 55), string_temp_current,
                  font=style.FONT_35, fill=style.BLACK)
        y = 100
        draw.text((250, y), string_feels_like,
                  font=style.FONT_15, fill=style.BLACK)
        draw.text((250, y + 20), string_wind,
                  font=style.FONT_15, fill=style.BLACK)
        draw.text(
            (250, y + 40), string_precip_percent, font=style.FONT_15, fill=style.BLACK
        )
        draw.text((250, y + 60), string_temp_max,
                  font=style.FONT_15, fill=style.BLACK)
        draw.text((250, y + 80), string_temp_min,
                  font=style.FONT_15, fill=style.BLACK)

        draw.text((125, 218), last_update_string,
                  font=style.FONT_15, fill=style.BLACK)

        # Weather Forcast
        # Tomorrow
        icon_file = nx_icon + ".png"
        icon_image = Image.open(os.path.join(config.ICON_DIR, icon_file))
        icon_image = icon_image.resize((130, 130))
        template.paste(icon_image, (435, 50))
        draw.text((450, 20), "Tomorrow", font=style.FONT_22, fill=style.BLACK)
        draw.text((415, 180), nx_day_high,
                  font=style.FONT_15, fill=style.BLACK)
        draw.text((515, 180), nx_day_low, font=style.FONT_15, fill=style.BLACK)
        draw.text((460, 200), nx_precip_percent,
                  font=style.FONT_15, fill=style.BLACK)

        # Next Next Day Forcast
        icon_file = nx_nx_icon + ".png"
        icon_image = Image.open(os.path.join(config.ICON_DIR, icon_file))
        icon_image = icon_image.resize((130, 130))
        template.paste(icon_image, (635, 50))
        draw.text((625, 20), "Next-Next Day",
                  font=style.FONT_22, fill=style.BLACK)
        draw.text((615, 180), nx_nx_day_high,
                  font=style.FONT_15, fill=style.BLACK)
        draw.text((715, 180), nx_nx_day_low,
                  font=style.FONT_15, fill=style.BLACK)
        draw.text((660, 200), nx_nx_precip_percent,
                  font=style.FONT_15, fill=style.BLACK)

        # Dividing lines
        draw.line((400, 10, 400, 220), fill=style.BLACK, width=3)
        draw.line((600, 20, 600, 210), fill=style.BLACK, width=2)

        # Tide Info
        # Graph
        tidegraph = Image.open(os.path.join(config.PIC_DIR, "TideLevel.png"))
        template.paste(tidegraph, (125, 240))

        # Large horizontal dividing line
        h = 240
        draw.line((25, h, 775, h), fill=style.BLACK, width=3)

        # Daily tide times
        draw.text((30, 260), "Today's Tide",
                  font=style.FONT_22, fill=style.BLACK)

        # Display tide preditions
        y_loc = 300  # starting location of list
        # Iterate over preditions
        for index, row in peaks_troughs_df.iterrows():
            # For high tide
            if row["state"] == "HIGH TIDE":
                tide_time = index.strftime("%H:%M")
                tidestr = f"High: {tide_time}  {round(row['height'],1)}m"
            # For low tide
            elif row["state"] == "LOW TIDE":
                tide_time = index.strftime("%H:%M")
                tidestr = f"Low:  {tide_time} {round(row['height'],1)}m"

            # Draw to display image
            draw.text((40, y_loc), tidestr,
                      font=style.FONT_15, fill=style.BLACK)
            y_loc += 25  # This bumps the next prediction down a line

        # Save the image for display as PNG
        screen_output_file = os.path.join(config.PIC_DIR, "screen_output.png")
        template.save(screen_output_file)
        # Close the template file
        template.close()

        screen.write_to_screen(
            screen_output_file, config.REFRESH_INTERVAL * 60)


if __name__ == "__main__":
    main()
