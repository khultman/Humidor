# Humidor.py
# Load the collected data into a local database.
# Periodically sync the local DB to the cloud.

# This is designed to use the SI7021 sensor
# 3 Sensors will be used per humidor
# The TCA9548A will be used for I2C multiplexing

import Adafruit_GPIO.SPI as SPI

import logging

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import RPi.GPIO as GPIO

from SI7021 import SI7021
from SSD1306 import SSD1306_64_48
from TCA9548A import TCA9548A

from smbus2 import SMBus

import time

# Setup logging
logger = logging.getLogger('Humidor.py')
threshold = getattr(logging, loglevel.upper(), None)
if not isinstance(threshold, int):
    raise ValueError("Invalid log level: {0}".format(loglevel))
logger.basicConfig(filename='Humidor.log',level=threshold)

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

disp = SSD1306_64_48(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
multiplexor = TCA9548A(SMBus(busID))
sensor = SI7021(SMBus(busID))

degS = u'\N{DEGREE SIGN}'


def disp_sensor_data(humidity = 0, temp_f = 0, temp_c = 0):
	disp.begin()
	disp.clear()
	disp.display()
	width = disp.width
	height = disp.height
	image = Image.new('1', (width, height))

	padding = 2
	top = padding
	bottom = height-padding
	x = padding
	fontsize = 14

	humidity = "{0}%".format(round(humidity, 2))
	temp_f = "{0}{1}F".format(round(temp_f, 2),degS)
	temp_c = "{0}{1}C".format(round(temp_c, 2),degS)

	draw = ImageDraw.Draw(image)
	fontRH = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontsize)
	fontT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontsize-4)

	draw.text((x+1, top+4), humidity,  font=fontRH, fill=255)
	draw.text((x+6, top+20), temp_f, font=fontT, fill=255)
	draw.text((x+6, top+30), temp_c, font=fontT, fill=255)

	disp.image(image)
	disp.display()


def get_sensor_data():
	temp_c = [None]*(sensors + 1)
	temp_f = [None]*(sensors + 1)
	humidity = [None]*(sensors + 1)
	temp_c[sensors] = 0
	temp_f[sensors] = 0
	humidity[sensors] = 0

	for i in range(0, sensors):
		multiplexor.select_channel(i)
		temp_c[i] = sensor.get_temperature_c()
		temp_f[i] = sensor.get_temperature_f()
		humidity[i] = sensor.get_humidity()
		logger.debug("Channel {0}, temp_c {1}, temp_f {2}, humidity {3}".format(i, temp_c[i], temp_f[i], humidity[i]))
		temp_c[sensors] += temp_c[i]
		temp_f[sensors] += temp_f[i]
		humidity[sensors] += humidity[i]

	temp_c[sensors] = temp_c[sensors] / sensors
	temp_f[sensors] = temp_f[sensors] / sensors
	humidity[sensors] = humidity[sensors] / sensors

	return [temp_c, temp_f, humidity]


def read(channel = 0):
	multiplexor.select_channel(channel)
	temp_c = sensor.get_temperature_c()
	temp_f = sensor.get_temperature_f()
	humidity = sensor.get_humidity()
	logger.debug("Channel {0}, temp_c {1}, temp_f {2}, humidity {3}".format(channel, temp_c, temp_f, humidity))
	print("Statistics for sensor on channel : %d" %channel)
	print("Relative Humidity is : {0}%".format(round(humidity,2)))
	print("Temperature in Celsius is : {0}C".format(round(temp_c,2)))
	print("Temperature in Fahrenheit is : {0}F".format(round(temp_f,2)))
	print("")


def print_sensor_data(sensor_data = []):
	for i in range(0, sensors):
		print("Sensor data for channel {0}".format(i))
		print("Relative Humidity is {0}%".format( round(sensor_data[2][i],2) ))
		print("Temperatur in Celsius is {0}{1} C".format( round(sensor_data[0][i],2), degS ))
		print("Temperature in Fahrenheit is {0}{1} F".format( round(sensor_data[1][i],2), degS ))
		print("")

	print("Averaged sensor data")
	print("Relative Humidity is {0}%".format( round(sensor_data[2][sensors],2) ))
	print("Temperatur in Celsius is {0}{1} C".format( round(sensor_data[0][sensors],2), degS ))
	print("Temperature in Fahrenheit is {0}{1} F".format( round(sensor_data[1][sensors],2), degS ))
	print("")

try:
	while True:
		sensor_data = get_sensor_data()
		print_sensor_data(sensor_data)
		disp_sensor_data(sensor_data[2][sensors], sensor_data[1][sensors], sensor_data[0][sensors])
except KeyboardInterrupt:
	GPIO.cleanup()

