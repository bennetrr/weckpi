"""
Own module to controll libvlc for python (python-vlc).
Depends on python-vlc and vlc itself.
"""
import random
import xml.etree.ElementTree as etree

import vlc

XSPF_NAMESPACE = "http://xspf.org/ns/0/"


class VolumeError(Exception):
	"""Exception that is raised on incorrect volume values"""
	pass


class BasePlayer:
	def __init__(self, source, instance_arguments = ('--aout=alsa',)):
		"""
		Base class used by the other classes in the module
		:param source: The path to the media file / stream
		:param instance_arguments: arguments passed to libvlc
		"""
		self.source = source
		self.instance = vlc.Instance(instance_arguments)
		self.player = None

	def play(self):
		"""Play music"""
		self.player.play()

	def pause(self):
		"""Pause music"""
		self.player.pause()

	def stop(self):
		"""Stop music"""
		self.player.stop()

	def next(self):
		"""Play next track"""
		self.player.next()

	def previous(self):
		"""Play previous track"""
		self.player.previous()

	def set_volume(self, volume: int):
		"""
		Set volume
		:param volume: An integer in the range from 0 to 100
		:raise VolumeError: If volume is less than 0 or greater than 100
		"""
		if not 0 <= volume <= 100:
			raise VolumeError("Volume must be in the range from 0 to 100")
		self.player.get_media_player().audio_set_volume(volume)


class Playlist(BasePlayer):
	def __init__(self, source):
		"""
		Plays a playlist in the defined order
		:param source: The path to the media file / stream
		"""
		BasePlayer.__init__(self, source)
		self.player = self.instance.media_list_player_new()
		self.medialist = self.instance.media_list_new()
		self.load_playlist()
		self.player.set_media_list(self.medialist)

	def load_playlist(self):
		self.medialist.add_media(self.source)


class RandomPlaylist(Playlist):
	def load_playlist(self):
		media_locations = [
			element.text
			for element in
			etree.parse(self.source).findall("xspf:trackList/xspf:track/xspf:location", {"xspf": XSPF_NAMESPACE}, )
		]
		random.shuffle(media_locations)
		for media_location in media_locations:
			self.medialist.add_media(media_location)

	def neworder(self):
		"""Make a new randomized order"""
		while len(self.medialist) > 0:
			self.medialist.remove_index(0)
		self.load_playlist()

	def stop(self):
		"""Stop the music and make a new randomized order"""
		Playlist.stop(self)
		self.neworder()


class InternetRadio(BasePlayer):
	def __init__(self, source):
		"""
		Plays an internet stream
		:param source: The path to the media file / stream
		"""
		BasePlayer.__init__(self, source, "--input-repeat=-1")
		self.player = self.instance.media_player_new()
		media = self.instance.media_new(self.source)
		self.player.set_media(media)

	def next(self):
		pass

	def pause(self):
		pass

	def previous(self):
		pass
