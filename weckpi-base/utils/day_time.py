import time
"""Various functions for days, times and dates"""


def nextday(thisday: str):
	"""
	:param thisday: A day in the week like Mon, Tue, Wed etc.
	:return: The next day
	"""
	days = {'Mon': 'Tue', 'Tue': 'Wed', 'Wed': 'Thu', 'Thu': 'Fri', 'Fri': 'Sat', 'Sat': 'Sun', 'Sun': 'Mon'}
	return days[thisday]


def comparetimes(time1: str, time2: str):
	"""
	:param time1: Time in hh:mm format
	:param time2: Time in hh:mm format
	:returns: time1 &lt; time2 -> 1<br>
	time1 = time2 -> 2<br>
	time1 > time2 -> 3
	"""

	h1, min1 = time1.split(':')
	h2, min2 = time2.split(':')

	h1 = int(h1)
	min1 = int(min1)
	h2 = int(h2)
	min2 = int(min2)

	if h1 < h2:
		return 1
	elif h1 > h2:
		return 3
	elif h1 == h2:
		if min1 < min2:
			return 1
		elif min1 > min2:
			return 3
		elif min1 == min2:
			return 2
		else:
			raise ValueError('Could not compare times ' + str(min1) + ' and ' + str(min2))
	else:
		raise ValueError('Could not compare times ' + str(h1) + ' and ' + str(h2))


def timenow():
	"""Returns the current time"""
	return time.strftime('%H:%M', time.localtime())


def daynow():
	"""Returns the current day"""
	return time.strftime('%a', time.localtime())
