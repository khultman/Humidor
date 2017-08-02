# Humidor.py
# Load the collected data into a local database.
# Periodically sync the local DB to the cloud.

# This is designed to use the SI7021 sensor
# 3 Sensors will be used per humidor
# The TCA9548A will be used for I2C multiplexing


from smbus2 import SMBus
import time
from SI7021 import SI7021
from TCA9548A import TCA9548A

# The I2C Bus ID
busID = 1



# Channels (May be wrong)
chan0 = 0x04
chan1 = 0x05
chan2 = 0x06
chan3 = 0x07
chan4 = 0x08
chan5 = 0x09
chan6 = 0x10
chan7 = 0x11

multiplexor = TCA9548A(SMBus(busID))
sensor = SI7021(SMBus(busID))


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

for i in range(0, 3):
	read(i)
