
from time import sleep


class TCA9548A:
	# Multiplexer address
	TCA9548A = 0x70

	# Channels (May be wrong)
	chan0 = 0x04
	chan1 = 0x05
	chan2 = 0x06
	chan3 = 0x07
	chan4 = 0x08
	chan5 = 0x09
	chan6 = 0x10
	chan7 = 0x11

	def __init__(self, bus, sleep_interval = SLEEP_INTERVAL):
		self.bus = bus
		self.tca9548a = TCA9548A
		self.sleep = sleep_interval

	def select_channel(channel = 0):
