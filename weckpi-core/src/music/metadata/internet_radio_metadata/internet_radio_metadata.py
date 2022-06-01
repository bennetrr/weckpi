"""Tools for working with the metadata of internet radio stations"""
from abc import ABC, abstractmethod

from music.metadata.now_playing import NowPlaying


class InternetRadioMetadataApi(ABC):
    """
    An abstraction for interacting with the metadata API of internet radio providers

    This class is an abstract class, do not instantiate it directly!
    """

    @property
    @abstractmethod
    def now_playing(self) -> NowPlaying:
        """Get information about the song that is playing now"""

    @property
    @abstractmethod
    def station_image(self) -> str:
        """Get the image of the station"""

    @property
    @abstractmethod
    def song_ends(self) -> float:
        """Get the time when the next song is played"""
