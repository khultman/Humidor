

from Humidor import Humidor

import argparse
import logging

import RPi.GPIO as GPIO

import time


# Setup logging
parser = argparse.ArgumentParser()

threshold = getattr(logging, loglevel.upper(), None)
if not isinstance(threshold, int):
    raise ValueError("Invalid log level: {0}".format(loglevel))
logging.basicConfig(filename='Humidor.log',level=threshold)
logger = logging.getLogger('Humidor.py')

# The I2C Bus ID
busID = 1

# GPIO of SSD1306 Reset pin
RST = 24

# GPIO of SSD1306 Display DC
DC = 23

# SPI Port & Device
SPI_PORT = 0
SPI_DEVICE = 0

# The number of sensors, min 1 max 8 
# corresponds to TCA9548 Channels
# Sensors must start on channel 0 and increment from there
sensors = 3

humidor = Humidor(busID, sensors, RST, DC, SPI_PORT, SPI_DEVICE)
try:
	while True:
		sensor_data = humidor.get_sensor_data()
		humidor.print_sensor_data()
		humidor.disp_avg_sensor_data()
except KeyboardInterrupt:
	GPIO.cleanup()
