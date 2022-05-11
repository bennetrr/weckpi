#! /bin/env python
from RPLCD import i2c


class I2CDisplay:
	"""Own class for the module RPLCD.i2c
	For more information about the parameters see RPLCD.i2c docs
	https://rplcd.readthedocs.io/en/stable/getting_started.html#setup-i2c"""

	def __init__(self, cols: int, rows: int, charmap: str, i2c_expander: str, address: hex, port: int):
		self.lcd = i2c.CharLCD(i2c_expander, address, port = port, charmap = charmap, cols = cols, rows = rows)

	def write(self, text):
		"""
		Writes text to the display
		:param text: Text to write
		"""
		self.lcd.write_string(str(text))

	def newline(self):
		"""Sets cursor to next line"""
		self.lcd.crlf()

	def clear(self):
		"""Clears the display"""
		self.lcd.clear()

	def close(self):
		"""Disconnects the display"""
		self.lcd.close(clear = True)

	def backlight(self, state: bool):
		"""
		Turns the backlight on or off
		:param state: State of the backlight
		"""
		self.lcd.backlight_enabled = state
