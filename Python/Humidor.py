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

from SI7021 import SI7021
from SSD1306 import SSD1306_64_48
from TCA9548A import TCA9548A

from smbus2 import SMBus

import sys
import time

# Defaults

busID = 1		# i2c bus ID
RST = 24		# GPIO of SSD1306 Reset pin
DC = 23			# GPIO of SSD1306 Display DC
SPI_PORT = 0	# SPI Port
SPI_DEVICE = 0	# SPI Device
sensors = 3		# Number of sensor channels

if sys.version_info[0] < 3:
	reload(sys)
	sys.setdefaultencoding('utf-8')

class Humidor(object):
	def __init__(self, i2cBUS = busID, sensors = sensors, rst = RST, dc = DC, spiPort = SPI_PORT, spiDevice = SPI_DEVICE):
		self._log = logging.getLogger(__name__)
		self._logging_variables = {}
		self._logging_variables['instance_id'] = self.__class__.__name__
		self._degS = u'\N{DEGREE SIGN}'
		self._busID = i2cBUS
		self._rst = rst
		self._dc = dc
		self._spiPort = spiPort
		self._spiDevice = spiDevice
		self.sensors = sensors
		self._multiplexor = TCA9548A(SMBus(self._busID), 0.1)
		self._sensor = SI7021(SMBus(self._busID), 0.1)
		self._disp = disp = SSD1306_64_48(rst=self._rst, dc=self._dc, spi=SPI.SpiDev(self._spiPort, self._spiDevice, max_speed_hz=8000000))

	def _clear(self):
		self._sensor_data = [None] * 3

	# Shorthand method for displaying the averaged sensor data
	def disp_avg_sensor_data(self):
		self.disp_sensor_data(self._sensor_data[2][self.sensors], self._sensor_data[1][self.sensors], self._sensor_data[0][self.sensors])

	# Write the given sensor data to the screen
	def disp_sensor_data(self, humidity = 0, temp_f = 0, temp_c = 0):
		self._disp.begin()
		self._disp.clear()
		self._disp.display()
		width = self._disp.width
		height = self._disp.height
		image = Image.new('1', (width, height))

		padding = 2
		top = padding
		bottom = height-padding
		x = padding
		fontsize = 14

		humidity = "{0}%".format(round(humidity, 2))
		temp_f = "{0}{1}F".format(round(temp_f, 2),self._degS)
		temp_c = "{0}{1}C".format(round(temp_c, 2),self._degS)

		draw = ImageDraw.Draw(image)
		fontRH = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontsize)
		fontT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontsize-4)

		draw.text((x+1, top+4), humidity,  font=fontRH, fill=255)
		draw.text((x+6, top+20), temp_f, font=fontT, fill=255)
		draw.text((x+6, top+30), temp_c, font=fontT, fill=255)

		self._disp.image(image)
		self._disp.display()

	# Reads the sensor data from all sensor channels
	# Returns multidimensional list for external processing
	# Stores data to self._sensor_data for internal processing
	def get_sensor_data(self):
		temp_c = [None]*(self.sensors + 1)
		temp_f = [None]*(self.sensors + 1)
		humidity = [None]*(self.sensors + 1)
		temp_c[self.sensors] = 0
		temp_f[self.sensors] = 0
		humidity[self.sensors] = 0

		for i in range(0, self.sensors):
			self._multiplexor.select_channel(i)
			temp_c[i] = self._sensor.get_temperature_c()
			temp_f[i] = self._sensor.get_temperature_f()
			humidity[i] = self._sensor.get_humidity()
			self._log.debug("Channel {0}, temp_c {1}, temp_f {2}, humidity {3}".format(i, temp_c[i], temp_f[i], humidity[i]), extra=[instance_id, self.__class__.__name__])
			temp_c[self.sensors] += temp_c[i]
			temp_f[self.sensors] += temp_f[i]
			humidity[self.sensors] += humidity[i]

		temp_c[self.sensors] = temp_c[self.sensors] / self.sensors
		temp_f[self.sensors] = temp_f[self.sensors] / self.sensors
		humidity[self.sensors] = humidity[self.sensors] / self.sensors

		self._sensor_data = [temp_c, temp_f, humidity]
		return [temp_c, temp_f, humidity]

	# Read the sensor data from an individual channel
	def read(self, channel = 0):
		self._multiplexor.select_channel(channel)
		temp_c = self._sensor.get_temperature_c()
		temp_f = self._sensor.get_temperature_f()
		humidity = self._sensor.get_humidity()
		self._log.debug("Channel {0}, temp_c {1}, temp_f {2}, humidity {3}".format(channel, temp_c, temp_f, humidity), extra=self._logging_variables)
		print("Statistics for sensor on channel : {0}".format(channel))
		print("Relative Humidity is : {0}%".format(round(humidity,2)))
		print("Temperature in Fahrenheit is : {0}F".format(round(temp_f,2)))
		print("Temperature in Celsius is : {0}C".format(round(temp_c,2)))
		print("")


	# Writes the data stored in self._sensor_data to stdout
	def print_sensor_data(self):
		for i in range(len(self._sensor_data)):
			print("Sensor data for channel {0}".format(i))
			print("Relative Humidity is {0}%".format(round(self._sensor_data[2][i],2)))
			print("Temperature in Fahrenheit is {0}{1} F".format(round(self._sensor_data[1][i],2),self._degS))
			print("Temperature in Celsius is {0}{1} C".format(round(self._sensor_data[0][i],2), self._degS))
			print("")
		print("Averaged sensor data")
		print("Relative Humidity is {0}%".format(round(self._sensor_data[2][self.sensors],2)))
		print("Temperature in Fahrenheit is {0}{1}F".format(round(self._sensor_data[1][self.sensors],2),self._degS))
		print("Temperature in Celsius is {0}{1}C".format(round(self._sensor_data[0][self.sensors],2),self._degS))
		print("")




