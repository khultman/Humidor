import logging
from time import sleep


class TCA9548A(object):
	# Multiplexer address
	TCA9548A = 0x70

	SLEEP_INTERVAL = 0.3

	# Channels (May be wrong)
	chan0 = 0x04
	chan1 = 0x05
	chan2 = 0x06
	chan3 = 0x07
	chan4 = 0x08
	chan5 = 0x09
	chan6 = 0x10
	chan7 = 0x11

	def __init__(self, bus, sleep_interval = SLEEP_INTERVAL, tca9548a = TCA9548A):
		self.bus = bus
		self.tca9548a = tca9548a
		self.sleep = sleep_interval
		self._log = logging.getLogger(__name__)
		self._logging_variables['instance_id'] = self.__class__.__name__

	def select_channel(self, channel = 0):
		self._log.debug("Changing TCA9548A multiplexor channel to {0}".format(channel), self._logging_variables)
		if channel == 1:
			self.bus.write_byte(self.tca9548a, self.chan1)
		elif channel == 2:
			self.bus.write_byte(self.tca9548a, self.chan2)
		elif channel == 3:
			self.bus.write_byte(self.tca9548a, self.chan3)
		elif channel == 4:
			self.bus.write_byte(self.tca9548a, self.chan4)
		elif channel == 5:
			self.bus.write_byte(self.tca9548a, self.chan5)
		elif channel == 6:
			self.bus.write_byte(self.tca9548a, self.chan6)
		elif channel == 7:
			self.bus.write_byte(self.tca9548a, self.chan7)
		else:
			self.bus.write_byte(self.tca9548a, self.chan0)
		sleep(self.sleep)


