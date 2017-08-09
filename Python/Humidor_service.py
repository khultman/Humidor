# Front-end the hardware interaction class
# Must run as root

import argparse

from Humidor import Humidor
import logging
from logger import MLOGGER
import sys
import time


# User Default Variables
cycle = 10			# The length (seconds) of each reporting cycle
display_cycles = 10	# The number of cycles to keep the LCD screen on
busID = 1			# The I2C Bus ID
RST = 24			# GPIO of SSD1306 Reset pin
DC = 23				# GPIO of SSD1306 Display DC
SPI_PORT = 0		# SPI Port
SPI_DEVICE = 0		# SPI Device
sensors = 3			# The number of sensors, min 1 max 8; corresponds to TCA9548 Channels; Sensors must start on channel 0 and increment from there
DoorPin = 5			# GPIO of Door Sensor
PirSensor = 6		# GPIO of PIR Sensor
PixelPin = 12		# Pin of NeoPixel Controller
PixelPixels = 30	# Number of NeoPixels on strip



class Humidor_Service(object):
	def __init__(self):
		self._logging_variables = {}
		self._logging_variables['instance_id'] = self.__class__.__name__
		self._log = logging.getLogger(self.__class__.__name__)
		self.humidor = Humidor(busID, sensors, RST, DC, SPI_PORT, SPI_DEVICE, display_cycles, PixelPixels, PixelPin)

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


	def main(self):
		loglevel, logtype, logfile = self.get_cli_args(sys.argv[1:])
		mlogger = MLOGGER(None, level=loglevel, logtype=logtype, filename=logfile)
		try:
			self._log.debug("Entering main loop", extra=self._logging_variables)
			while True:
				sensor_data = self.humidor.get_sensor_data()
				self.humidor.print_sensor_data()
				self.humidor.display_data()
				time.sleep(cycle)
		except KeyboardInterrupt:
			GPIO.cleanup()


if __name__ == '__main__':
	service = Humidor_Service()
	service.main()
	
