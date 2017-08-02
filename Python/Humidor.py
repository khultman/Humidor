# Humidor.py
# Load the collected data into a local database.
# Periodically sync the local DB to the cloud.

# This is designed to use the SI7021 sensor
# 3 Sensors will be used per humidor
# The TCA9548A will be used for I2C multiplexing


import smbus
import time

# The I2C Bus ID
busID = 1

# Multiplexer address
TCA9548A = 0x70

# SI7021 address
SI7021 = 0x40

# SI7021 Commands
readHumidity = 0xF5 # Read humidity, no hold
readTemp = 0xF3 # Read humidity, no hold

# Channels (May be wrong)
chan0 = 0x04
chan1 = 0x05
chan2 = 0x06
chan3 = 0x07
chan4 = 0x08
chan5 = 0x09
chan6 = 0x10
chan7 = 0x11

# Sleep Interval, may need to be adjusted for different bus clock speeds
sleepInterval = 0.3

def sleep():
	time.sleep(sleepInterval)

def getTemp():
	bus = smbus.SMBus(busID)
	bus.write_byte(SI7021, readTemp)
	sleep()
	data0 = bus.read_byte(SI7021)
	data1 = bus.read_byte(SI7021)
	return ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85

def getHumidity():
	bus = smbus.SMBus(busID)
	bus.write_byte(SI7021, readHumidity)
	sleep()
	data0 = bus.read_byte(SI7021)
	data1 = bus.read_byte(SI7021)
	return ((data0 * 256 + data1) * 125 / 65536.0) - 6


def selectChannel(channel = chan0):
	smbus = smbus.SMBus(busID)
	bus.write_byte(TCA9548A, 0x00)
	sleep()
	bus.write_byte(TCA9548A, channel)


humidity = getHumidity()
temp = getTemp()

print "Relative Humidity is : %.2f %%" %humidity
print "Temperature in Celsius is : %.2f C" %temp
print "Temperature in Fahrenheit is : %.2f F" %(temp * 1.8 + 32)