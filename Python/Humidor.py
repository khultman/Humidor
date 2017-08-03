# Humidor.py
# Load the collected data into a local database.
# Periodically sync the local DB to the cloud.

# This is designed to use the SI7021 sensor
# 3 Sensors will be used per humidor
# The TCA9548A will be used for I2C multiplexing

import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from SI7021 import SI7021
from SSD1306 import SSD1306_64_48
from TCA9548A import TCA9548A

from smbus2 import SMBus

import time

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

def disp_sensor_data(humidity = 0, temp_f = 0):
	disp.begin()
	disp.clear()
	disp.display()
	width = disp.width
	height = disp.height
	image = Image.new('1', (width, height))

	padding = 2
	shape_width = 20
	top = padding
	bottom = height-padding
	x = padding

	humidity = "Humidity: {0}% RH".format(humidity)
	temp_f = "Temp: {0} F".format(temp_f)

	draw = ImageDraw.Draw(image)
	font = ImageFont.load_default()
	draw.text((x, top),    humidity,  font=font, fill=255)
	draw.text((x, top+20), temp_f, font=font, fill=255)

	disp.image(image)
	disp.display()


def get_sensor_data():
	temp_c = [None]*max(sensors+1)
	temp_f = [None]*max(sensors+1)
	humidity = [None]*max(sensors+1)
	temp_c[sensors] = 0
	temp_f[sensors] = 0
	humidity[sensors] = 0

	for i in range(0, sensors):
		multiplexor.select_channel(i)
		temp_c[i] = sensor.get_temperature_c()
		temp_f[i] = sensor.get_temperature_f()
		humidity[i] = sensor.get_humidity()
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
	print("Statistics for sensor on channel : %d" %channel)
	print("Relative Humidity is : %.2f %%" %humidity)
	print("Temperature in Celsius is : %.2f C" %temp_c)
	print("Temperature in Fahrenheit is : %.2f F" %temp_f)
	print("")

sensor_data = get_sensor_data()
for i in range(0, sensors):
	print("Sensor data for channel {0}".format(i))
	print("Relative Humidity is {0}%%".format(sensor_data[2][i]))
	print("Temperatur in Celsius is {0} C".format(sensor_data[0][i]))
	print("Temperature in Fahrenheit is {0} F".format(sensor_data[1][i]))
	print("")

print("Averaged sensor data")
print("Relative Humidity is {0}%%".format(sensor_data[2][sensors]))
print("Temperatur in Celsius is {0} C".format(sensor_data[0][sensors]))
print("Temperature in Fahrenheit is {0} F".format(sensor_data[1][sensors]))
print("")

disp_sensor_data(sensor_data[2][sensors], sensor_data[1][sensors])

