from neopixel import *
import time

# LED strip configuration:
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (12 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering


class Pixel(object):
	def __init__(	self, count = LED_COUNT, pin = LED_PIN, frequency = LED_FREQ_HZ, 
					dma = LED_DMA, brightness = LED_BRIGHTNESS, invert = LED_INVERT,
					channel = LED_CHANNEL, strip = LED_STRIP):
		self._led_count = count
		self._led_pin = pin
		self._led_frequency = frequency
		self._led_dma = dma
		self._led_brightness = brightness
		self._led_invert = invert
		self._led_channel = channel
		self._led_strip = strip
		self._strip = Adafruit_NeoPixel(self._led_count, self._led_pin, self._led_frequency, 
										self._led_dma, self._led_invert, self._led_brightness,
										self._led_channel, self._led_strip)
		self._strip.begin()

	
	def color_wipe(self, color, wait_ms = 50):
		# Wipe color across display a pixel at a time.
		for i in range(self._strip.numPixels()):
			self._strip.setPixelColor(i, color)
			self._strip.show()
			time.sleep(wait_ms/1000.0)

	def red_wipe(self):
		self.color_wipe(Color(255, 0, 0))

	def blue_wipe(self):
		self.color_wipe(Color(0, 255, 0))

	def green_wipe(self):
		self.color_wipe(Color(0, 0, 255))

	def white_wipe(self):
		self.color_wipe(Color(127, 127, 127))



	def chase(self, color, wait_ms=50, iterations=10):
		# Movie theater light style chaser animation.
		for j in range(iterations):
			for q in range(3):
				for i in range(0, self._strip.numPixels(), 3):
					self._strip.setPixelColor(i+q, color)
				strip.show()
				time.sleep(wait_ms/1000.0)
				for i in range(0, strip.numPixels(), 3):
					self._strip.setPixelColor(i+q, 0)

	def red_chase(self):
		self.chase(Color(255, 0, 0))

	def blue_chase(self):
		self.chase(Color(0, 255, 0))

	def green_chase(self):
		self.chase(Color(0, 0, 255))

	def white_chase(self):
		self.chase(Color(127, 127, 127))

	def rainbow_chase(self, wait_ms=50):
		# Rainbow movie theater light style chaser animation.
		for j in range(256):
			for q in range(3):
				for i in range(0, self._strip.numPixels(), 3):
					self._strip.setPixelColor(i+q, wheel((i+j) % 255))
				self._strip.show()
				time.sleep(wait_ms/1000.0)
				for i in range(0, self._strip.numPixels(), 3):
					self._strip.setPixelColor(i+q, 0)



	def wheel(self, pos):
		# Generate rainbow colors across 0-255 positions.
		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)

	def rainbow(self, wait_ms=20, iterations=1):
		# Draw rainbow that fades across all pixels at once.
		for j in range(256*iterations):
			for i in range(self._strip.numPixels()):
				self._strip.setPixelColor(i, wheel((i+j) & 255))
			self._strip.show()
			time.sleep(wait_ms/1000.0)

	def rainbow_cycle(self, wait_ms=20, iterations=5):
		# Draw rainbow that uniformly distributes itself across all pixels.
		for j in range(256*iterations):
			for i in range(self._strip.numPixels()):
				self._strip.setPixelColor(i, self.wheel((int(i * 256 / self._strip.numPixels()) + j) & 255))
			self._strip.show()
			time.sleep(wait_ms/1000.0)

	


