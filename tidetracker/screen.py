from datetime import datetime
import os
import sys
import time

from PIL import Image

sys.path.append("lib")

from PIL import ImageDraw
from waveshare_epd import epd7in5_V2
from tidetracker import config, style


# Initialize and clear screen
class Screen:
    def __init__(self):
        print("Initializing and clearing screen.")
        epd = epd7in5_V2.EPD()  # Create object for display functions
        epd.init()
        epd.Clear()
        self.epd = epd

    # define funciton for writing image and sleeping for specified time
    def write_to_screen(self, image, sleep_seconds):
        print("Writing to screen.")  # for debugging
        # Create new blank image template matching screen resolution
        h_image = Image.new("1", (self.epd.width, self.epd.height), 255)
        # Open the template
        screen_output_file = Image.open(os.path.join(config.PIC_DIR, image))
        # Initialize the drawing context with template as background
        h_image.paste(screen_output_file, (0, 0))
        self.epd.display(self.epd.getbuffer(h_image))
        # Sleep
        self.epd.sleep()  # Put screen to sleep to prevent damage
        print("Sleeping for " + str(sleep_seconds) + ".")
        time.sleep(sleep_seconds)  # Determines refresh rate on data
        self.epd.init()  # Re-Initialize screen

    # define function for displaying error
    def display_error(self, error_source):
        # Display an error
        print("Error in the", error_source, "request.")
        # Initialize drawing
        error_image = Image.new("1", (self.epd.width, self.epd.height), 255)
        # Initialize the drawing
        draw = ImageDraw.Draw(error_image)
        draw.text(
            (100, 150), error_source + " ERROR", font=style.FONT_50, fill=style.BLACK
        )
        draw.text(
            (100, 300), "Retrying in 30 seconds", font=style.FONT_22, fill=style.BLACK
        )
        current_time = datetime.now().strftime("%H:%M")
        draw.text(
            (300, 365),
            "Last Refresh: " + str(current_time),
            font=style.FONT_50,
            fill=style.BLACK,
        )
        # Save the error image
        error_image_file = "error.png"
        error_image.save(os.path.join(config.PIC_DIR, error_image_file))
        # Close error image
        error_image.close()
        # Write error to screen
        self.write_to_screen(error_image_file, 30)
