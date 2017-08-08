
import argparse

from Humidor import Humidor
import logging
from logger import MLOGGER

import RPi.GPIO as GPIO
import sys
import time


# Defaults
busID = 1			# The I2C Bus ID
RST = 24			# GPIO of SSD1306 Reset pin
DC = 23				# GPIO of SSD1306 Display DC
SPI_PORT = 0		# SPI Port
SPI_DEVICE = 0		# SPI Device
sensors = 3			# The number of sensors, min 1 max 8; corresponds to TCA9548 Channels; Sensors must start on channel 0 and increment from there
DoorPin = 5			# GPIO of Door Sensor


class Humidor_Service(object):
	def __init__(self):
		self._logging_variables = {}
		self._logging_variables['instance_id'] = self.__class__.__name__
		self._log = logging.getLogger(self.__class__.__name__)

	def get_cli_args(self, args=None):
		parser = argparse.ArgumentParser(description='Run the Humidor service')
		parser.add_argument('-lv', '--loglevel',
							type=str,
							help='Log Level {INFO,DEBUG,ERROR} Default = INFO',
							choices={'INFO', 'DEBUG', 'ERROR'},
							default='INFO')
		parser.add_argument('-lt', '--logtype',
							type=str,
							help='Log to  {CONSOLE,FILE,BOTH,NONE} Default = CONSOLE',
							choices={'CONSOLE', 'FILE', 'BOTH', 'NONE'},
							default='CONSOLE')
		parser.add_argument('-lf', '--logfile',
							type=str,
							help='Log filename Default = Humidor.log',
							default='Humidor.log')
		results = parser.parse_args(args)
		return (results.loglevel,
				results.logtype,
				results.logfile)

	def door_open(self, channel):
		self._log.warn("Door Opened, channel {0}".format(channel), extra=self._logging_variables)

	def door_closed(self, channel):
		self._log.warn("Door Closed, channel {0}".format(channel), extra=self._logging_variables)

	def main(self):
		loglevel, logtype, logfile = self.get_cli_args(sys.argv[1:])
		mlogger = MLOGGER(None, level=loglevel, logtype=logtype, filename=logfile)
		humidor = Humidor(busID, sensors, RST, DC, SPI_PORT, SPI_DEVICE)
		try:
			GPIO.setup(DoorPin, GPIO.IN)
			GPIO.add_event_detect(DoorPin, GPIO.RISING, callback=self.door_open, bouncetime=300)
			#GPIO.add_event_detect(DoorPin, GPIO.RISING, callback=self.door_closed, bouncetime=300)
			self._log.debug("Entering main loop", extra=self._logging_variables)
			while True:
				sensor_data = humidor.get_sensor_data()
				humidor.print_sensor_data()
				humidor.disp_avg_sensor_data()
				time.sleep(10)
		except KeyboardInterrupt:
			GPIO.cleanup()


if __name__ == '__main__':
	service = Humidor_Service()
	service.main()
	
