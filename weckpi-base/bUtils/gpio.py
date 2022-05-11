from time import sleep
import threading
from RPi import GPIO

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

class Button:
	def __init__(self, pin: int):
		"""
		Use a GPIO pin as input / button
		:param pin: A number of a GPIO pin (mode BOARD)
		"""
		GPIO.setup(pin, GPIO.IN)
		self.pin = pin

	def getstate(self):
		""":return: State of the GPIO pin"""
		return GPIO.input(self.pin)


class Output:
	def __init__(self, pin: int):
		"""
		Use a GPIO pin as output
		:param pin: A number of a GPIO pin (mode BOARD)
		"""
		GPIO.setup(pin, GPIO.OUT)
		self.pin = pin

	def setstate(self, state: bool):
		"""
		Change the state of the specifed GPIO pin
		:param state: State of the GPIO pin
		"""
		GPIO.output(self.pin, state)


class LED(Output):
	def __init__(self, pin: int, isreversed: bool):
		"""
		Use a GPIO pin as output for a led
		:param pin: A number of a GPIO pin (mode BOARD)
		"""
		Output.__init__(self, pin)
		self.isreversed = isreversed
		self.thread_stop = False
		self.thread = threading.Thread()

	def setledstate(self, state: bool):
		"""
		Change the state of the LED
		:param state: State of the LED
		"""
		if self.isreversed:
			self.setstate(not state)
		else:
			self.setstate(state)

	def flash(self, runs, delay):
		"""
		Let the LED flash
		:param runs: How often the LED should flash
		:param delay: How long the program waits between turn the LED on / off
		"""
		while runs > 0 and not self.thread_stop:
			self.setledstate(True)
			sleep(delay)
			self.setledstate(False)
			sleep(delay)
			runs = runs - 1
		else:
			return

	def flash_bg(self, runs, delay):
		"""
		Let the LED flash in a seperate Thread
		:param runs: How often the LED should flash
		:param delay: How long the program waits between turn the LED on / off
		"""
		self.thread_stop = False
		self.thread = threading.Thread(target = self.flash, args = (runs, delay))
		self.thread.start()


	def stop_flash_bg(self):
		self.thread_stop = True
		self.thread.join()


def clean():
	"""Clean the GPIO configuration"""
	GPIO.cleanup()
