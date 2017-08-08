
import argparse

from Humidor import Humidor
from logger import MLOGGER

import RPi.GPIO as GPIO
import sys
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



def get_cli_args(args=None):
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




if __name__ == '__main__':
	loglevel, logtype, logfile = get_cli_args(sys.argv[1:])
	logger = MLOGGER('Humidor_Service', level=loglevel, logtype=logtype, filename=logfile)
	humidor = Humidor(busID, sensors, RST, DC, SPI_PORT, SPI_DEVICE)
	try:
		while True:
			sensor_data = humidor.get_sensor_data()
			humidor.print_sensor_data()
			humidor.disp_avg_sensor_data()
	except KeyboardInterrupt:
		GPIO.cleanup()
