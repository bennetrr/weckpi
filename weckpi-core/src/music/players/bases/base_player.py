"""The base for every vlc player"""
from abc import ABC, abstractmethod
from typing import Optional

import vlc

from music.metadata.now_playing import NowPlaying


class BasePlayer(ABC):
    """
    The base for every vlc player

    This class is an abstract class, do not instantiate it directly!
    """
    instance: vlc.Instance
    player: vlc.MediaPlayer

    def __init__(self, *args: str):
        """
        The base for every vlc player

        :param args: Arguments to pass to vlc.
        For possible arguments, see vlc --help
        """
        self.instance = vlc.Instance(args)
        self.player = self.instance.media_player_new()

    def play(self) -> None:
        """Start the playback of the media"""
        self.player.play()

    def pause(self) -> None:
        """Pause the playback of the media"""
        self.player.pause()

    def stop(self) -> None:
        """Stop the playback of the media and reset the media"""
        self.player.stop()

    @abstractmethod
    def next(self) -> None:
        """Jump to the next item in the playlist"""

    @abstractmethod
    def previous(self) -> None:
        """Jump to the previous item in the playlist"""

    @property
    @abstractmethod
    def now_playing(self) -> Optional[NowPlaying]:
        """Get information about the song that is playing now"""

    @property
    def is_playing(self) -> bool:
        """Get if the player is now playing"""
        return self.player.is_playing()

    @property
    def position(self) -> float:
        """Get the position of the playback in percent"""
        return self.player.get_position() * 100

    @property
    def volume(self) -> int:
        """Get the volume of the player"""
        return self.player.audio_get_volume()

    @volume.setter
    def volume(self, volume) -> None:
        """
        Set the volume of the player

        :param volume: The volume in percent (0 = mute, 100 = 0dB)
        :raises ValueError: If the given volume is out of range
        """
        if volume < 0 or volume > 100:
            raise ValueError(f'The volume is out of range (0≰{volume}≰100)')
        self.player.audio_set_volume(volume)

    def __str__(self):
        """Return the now playing information as a string"""
        return str(self.now_playing)
