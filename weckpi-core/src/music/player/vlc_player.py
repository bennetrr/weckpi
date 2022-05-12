"""The base for a vlc player"""
import vlc
from typing import Union


class BasePlayer:
    instance: vlc.Instance
    player: Union[vlc.MediaListPlayer, vlc.MediaPlayer]
    media_list: vlc.MediaList

    def __init__(self, args: tuple[str] = ()):
        self.instance = vlc.Instance(args)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def next(self):
        ...

    def previous(self):
        ...

    def set_volume(self, volume):
        self.player.audio_set_volume(volume)

    def get_volume(self):
        return self.player.audio_get_volume()

    volume = property(get_volume, set_volume)
