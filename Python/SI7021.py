import logging
from time import sleep

class SI7021(object):
	# SI7021 address
	SI7021 				= 0x40			# Default Address, AFAIK Cannot be overridden

	# SI7021 Commands
	READ_HUMIDITY_HM	= 0xE5 			# Read humidity, hold master mode
	READ_HUMIDITY_NH	= 0xF5 			# Read humidity, no hold master mode
	READ_TEMP_HM		= 0xE3 			# Read temperature, hold master mode
	READ_TEMP_NH		= 0xF3 			# Read temperature, no hold master mode
	READ_TEMP_PREV		= 0xE0 			# Read temperature from previous RH Measurement
	DEV_RESET			= 0xFE 			# Reset sensor
	WRITE_UR1			= 0xE6 			# Write to RH/T User Register 1
	READ_UR1			= 0xE7 			# Read from RH/T User Register 1
	READ_ELECTRONIC_ID1	= [0xFA, 0x0F]	# Read Electronic ID 1st Byte
	READ_ELECTRONIC_ID2	= [0xFC, 0xC9]	# Read Electronic ID 2nd Byte
	READ_FIRMWARE		= [0x84, 0xB8]	# Read Firmware Revision

	# Sleep interval
	SLEEP_INTERVAL		= 0.3			# This may need to be overridden depending on bus speed

	def __init__(self, bus, sleep_interval = SLEEP_INTERVAL, si7021 = SI7021):
		self.bus = bus
		self.si7021 = si7021
		self.sleep = sleep_interval
		self._log = logging.getLogger(__name__)
		self._logging_variables = {}
		self._logging_variables['instance_id'] = self.__class__.__name__

	# This doesn't work, here as a placeholder
	def _dontcall_get_firmware(self):
		self.reset()
		self.bus.write_i2c_block_data(self.si7021, 0, self.READ_FIRMWARE)
		sleep(self.sleep)
		firmware = self.bus.read_i2c_block_data(self.si7021, 0)
		return firmware

	# Read the temp from the sensor
	def get_temperature_c(self):
		self.reset()
		self.bus.write_byte(self.si7021, self.READ_TEMP_NH)
		sleep(self.sleep)
		temp = self.bus.read_word_data(self.si7021, self.READ_TEMP_PREV)
		self._log.debug("Temp raw value :: {0}".format(temp), extra=self._logging_variables)
		temp = ((temp & 0xff) << 8) | (temp >> 8)
		temp = 175.72 * temp / 65536. - 46.85
		self._log.debug("Temp computed value :: {0}".format(temp), extra=self._logging_variables)
		return temp

	# Shorthand for computing to fahrenheit
	def get_temperature_f(self):
		temp = self.get_temperature_c()
		temp = temp * 1.8 + 32
		self._log.debug("Temp computed value fahrenheit :: {0}".format(temp), extra=self._logging_variables)
		return temp

	# Read the humidity from the sensor
	def get_humidity(self):
		# Hold master mode not working reliably
		#humidity = self.bus.read_word_data(self.si7021, self.READ_HUMIDITY_HM)
		#humidity = ((humidity & 0xff) << 8) | (humidity >> 8)
		#humidity = 125. * humidity  / 65536. - 6
		self.reset()
		self.bus.write_byte(self.si7021, self.READ_HUMIDITY_NH)
		sleep(self.sleep)
		h1 = self.bus.read_byte(self.si7021)
		h2 = self.bus.read_byte(self.si7021)
		self._log.debug("Raw humidity data :: {0} & {1}".format(h1,h2), extra=self._logging_variables)
		humidity = ((h1 * 256 + h2) * 125 / 65536.0) - 6
		self._log.debug("Computed humidity data :: {0}".format(humidity), extra=self._logging_variables)
		if humidity <= 0:
			self._log.warn("Humidity reported irrationally, sensor may be damaged or broken. Humidity: {0}".format(humidity), extra=self._logging_variables)
		return humidity

	def reset(self):
		self.bus.write_byte(self.si7021, self.DEV_RESET)
		sleep(self.sleep)

