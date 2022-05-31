"""The base for every vlc player"""
from abc import ABC, abstractmethod
from pathlib import Path

import vlc

from music.metadata import NowPlaying, InternetRadioMetadataApi


def add_argument(args: tuple[str], arg: str) -> tuple[str]:
    """
    Add a new argument to the list of arguments

    :param args: The old list of arguments
    :param arg: The new argument
    :return: The new list of arguments
    """
    list_args = list(args)
    list_args.append(arg)
    return tuple(list_args)


class BasePlayer(ABC):
    """
    The base for every vlc player

    This class is an abstract class, do not instantiate it directly!
    """
    instance: vlc.Instance
    player: vlc.MediaListPlayer | vlc.MediaPlayer
    media: vlc.MediaList | vlc.Media
    media_source = str | Path

    def __init__(self, *args: str):
        """
        The base for every vlc player

        :param args: Arguments to pass to vlc.
        For possible arguments, see the help of the vlc cli.
        """
        self.instance = vlc.Instance(args)

    @abstractmethod
    def set_media(self, media_source: str | Path, now_playing: NowPlaying | InternetRadioMetadataApi) -> None:
        """Set the media source"""

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
    def now_playing(self) -> NowPlaying:
        """Get information about the song that is playing now"""

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
