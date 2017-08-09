# Front-end the hardware interaction class
# Must run as root

import argparse

from Humidor import Humidor
import logging
from logger import MLOGGER
import sys
import time


# User Default Variables ;; move to command line args later
# cycle = 10			# The length (seconds) of each reporting cycle
# display_cycles = 10	# The number of cycles to keep the LCD screen on
# busID = 1			# The I2C Bus ID
# RST = 24			# GPIO of SSD1306 Reset pin
# DC = 23				# GPIO of SSD1306 Display DC
# SPI_PORT = 0		# SPI Port
# SPI_DEVICE = 0		# SPI Device
# sensors = 3			# The number of sensors, min 1 max 8; corresponds to TCA9548 Channels; Sensors must start on channel 0 and increment from there
# DoorPin = 5			# GPIO of Door Sensor
# PirSensor = 6		# GPIO of PIR Sensor
# PixelPin = 12		# Pin of NeoPixel Controller
# PixelPixels = 30	# Number of NeoPixels on strip



class Humidor_Service(object):
	def __init__(self):
		self._args = self.get_cli_args(sys.argv[1:])
		self.mlogger = MLOGGER(None, level=self._args.loglevel, logtype=self._args.logtype, filename=self._args.logfile)
		self._logging_variables = {}
		self._logging_variables['instance_id'] = self.__class__.__name__
		self._log = logging.getLogger(self.__class__.__name__)
		self.humidor = Humidor(	self._args.busID, self._args.sensors,
								self._args.RST, self._args.DC, self._args.SPI_PORT, self._args.SPI_DEVICE, self._args.display_cycles,
								self._args.PixelPixels, self._args.PixelPin, self._args.DoorPin, self._args.PirSensor)

	def get_cli_args(self, args=None):
		parser = argparse.ArgumentParser(description='Run the Humidor service')
		# Basic Config
		basic_cfg = parser.add_argument_group('Humidor Configuration')
		basic_cfg.add_argument(	"-cy", "--cycle",
								help="Time in seconds between each loop cycle, defaults to 10",
								type=int,
								action="store",
								dest="cycle",
								default=10)
		basic_cfg.add_argument(	"-dcy", "--displaycycles",
								help="How many cycles should the display be on after motion, defaults to 10",
								type=int,
								action="store",
								dest="display_cycles",
								default=10)
		basic_cfg.add_argument(	"-bid", "--busID",
								help="The I2C Bus ID, default 1",
								type=int,
								action="store",
								dest="busID",
								default=1)
		basic_1306 = parser.add_argument_group('SSD1306 Configuration')
		basic_1306.add_argument("-rst",
								help="GPIO of SSD1306 Reset pin, default 24",
								type=int,
								action="store",
								dest="RST",
								default="24")
		basic_1306.add_argument("-dc",
								help="GPIO of SSD1306 Display DC Pin, default 23",
								type=int,
								action="store",
								dest="DC",
								default="23")
		basic_1306.add_argument("-sp", "--spi_port",
								help="SPI Port, default 0",
								type=int,
								action="store",
								dest="SPI_PORT",
								default=0)
		basic_1306.add_argument("-sd", "--spi_device",
								help="SPI Device, default 0",
								type=int,
								action="store",
								dest="SPI_DEVICE",
								default=0)
		basic_sens = parser.add_argument_group("Sensor Configuration")
		basic_sens.add_argument("-ss", "--sensors",
								help="The number of sensors, min 1 max 8; corresponds to TCA9548 channels, starting on 0",
								type=int,
								action="store",
								dest="sensors",
								choices=range(1,9),
								default=3)
		basic_gpio = parser.add_argument_group("GPIO Configuration")
		basic_gpio.add_argument("-dp", "--doorpin",
								help="GPIO of Door Pin, default 5",
								type=int,
								action="store",
								dest="DoorPin",
								default=5)
		basic_gpio.add_argument("-pr", "--pirpin",
								help="GPIO of PIR Pin, default 6",
								type=int,
								action="store",
								dest="PirSensor",
								default=6)
		basic_pix = parser.add_argument_group('Neopixel Configuration')
		basic_pix.add_argument(	"-pp", "--pixelpin",
								help="GPIO of NeoPixel Controller",
								type=int,
								action="store",
								dest="PixelPin",
								default="12")
		basic_pix.add_argument(	"--pixels",
								help="The number of pixels connected to the strip",
								type=int,
								action="store",
								dest="PixelPixels",
								default=30)
		basic_pix.add_argument(	"--pixelchannel",
								help="PWM Channel of NeoPixel",
								type=int,
								choices=[0,1],
								action="store",
								dest="pixel_channel",
								default=0)
		# AWS IoT Config
		aws = parser.add_argument_group('AWS IoT')
		aws.add_argument(	"-e", "--endpoint",
							help="Your AWS IoT custom endpoint",
							action="store",
							required=True,
							dest="aws_Endpoint")
		aws.add_argument(	"-r", "--rootCA",
							help="Root CA file path",
							action="store",
							required=True,
							dest="aws_rootCAPath")
		aws_meg = aws.add_mutually_exclusive_group()
		aws_meg.add_argument(	"-w", "--websocket",
								help="Use MQTT over WebSocket",
								action="store_true",
								dest="aws_useWebsocket",
								default=False)
		aws_meg_cert = aws_meg.add_argument_group('Certificate Authentication')
		aws_meg_cert.add_argument(	"-c", "--cert",
									help="Certificate file path",
									action="store",
									dest="aws_certificatePath")
		aws_meg_cert.add_argument(	"-k", "--key",
									help="Private key file path",
									action="store",
									dest="aws_privateKeyPath")
		aws.add_argument(	"-id", "--clientId",
							help="Targeted client id",
							action="store",
							dest="aws_clientId",
							default="humidor")
		aws.add_argument(	"-t", "--topic",
							help="Targeted topic",
							action="store",
							dest="aws_topic",
							default="humidor")
		# Logging Elements
		log = parser.add_argument_group('Logging')
		log.add_argument('-lv', '--loglevel',
							type=str,
							help='Log Level {INFO,DEBUG,ERROR} Default = INFO',
							choices={'INFO', 'DEBUG', 'ERROR'},
							dest='loglevel',
							default='INFO')
		log.add_argument('-lt', '--logtype',
							type=str,
							help='Log to  {CONSOLE,FILE,BOTH,NONE} Default = CONSOLE',
							choices={'CONSOLE', 'FILE', 'BOTH', 'NONE'},
							dest='logtype',
							default='CONSOLE')
		log.add_argument('-lf', '--logfile',
							type=str,
							help='Log filename Default = Humidor.log',
							dest='logfile',
							default='Humidor.log')
		results = parser.parse_args(args)
		return results


	def main(self):
		try:
			self._log.debug("Entering main loop", extra=self._logging_variables)
			while True:
				sensor_data = self.humidor.get_sensor_data_dict()
				self.humidor.print_sensor_data()
				self.humidor.display_data()
				time.sleep(self._args.cycle)
		except KeyboardInterrupt:
			self.humidor.cleanup()
			pass


if __name__ == '__main__':
	service = Humidor_Service()
	service.main()
	
