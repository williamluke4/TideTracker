from os import path

from PIL import ImageFont

from tidetracker import config

# Set the font sizes
FONT_15 = ImageFont.truetype(path.join(config.FONT_DIR, "Font.ttc"), 15)
FONT_20 = ImageFont.truetype(path.join(config.FONT_DIR, "Font.ttc"), 20)
FONT_22 = ImageFont.truetype(path.join(config.FONT_DIR, "Font.ttc"), 22)
FONT_30 = ImageFont.truetype(path.join(config.FONT_DIR, "Font.ttc"), 30)
FONT_35 = ImageFont.truetype(path.join(config.FONT_DIR, "Font.ttc"), 35)
FONT_50 = ImageFont.truetype(path.join(config.FONT_DIR, "Font.ttc"), 50)
FONT_60 = ImageFont.truetype(path.join(config.FONT_DIR, "Font.ttc"), 60)
FONT_100 = ImageFont.truetype(path.join(config.FONT_DIR, "Font.ttc"), 100)
FONT_160 = ImageFont.truetype(path.join(config.FONT_DIR, "Font.ttc"), 160)

# Set the colors
BLACK = "rgb(0,0,0)"
WHITE = "rgb(255,255,255)"
GREY = "rgb(235,235,235)"
