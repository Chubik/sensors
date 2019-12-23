#!/usr/bin/python

import sys
sys.path.insert(1, '../drivers/')

import Adafruit_DHT
import time
import epd2in7

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

W = epd2in7.EPD_WIDTH
H = epd2in7.EPD_HEIGHT
size = (W, H)

epd = epd2in7.EPD()
epd.init()


teenyfont = ImageFont.truetype(
    '/usr/share/fonts/truetype/freefont/FreeSans.ttf', 12)


def printMaskToEinkScreen(tempstr):
    lastUpdated = time.strftime('%a %d.%m %H:%M')

    mask = Image.new('1', (H,W), 255)    # 255: clear the image with white; H,W for rotation
    draw = ImageDraw.Draw(mask)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 14)

    line = 1
    draw.text((1,line), tempstr, font=font, fill=0)

    rotatedMask = mask.rotate(90, expand=True)
    epd.display_frame(epd.get_frame_buffer(rotatedMask))
    print('Display successfully refreshed at {}'.format(time.strftime('%d%m%y-%H:%M:%S')))


while True:

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    printMaskToEinkScreen('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
    time. sleep(1)
    