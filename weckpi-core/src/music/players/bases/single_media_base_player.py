"""The base for every vlc player for single media sources"""
import logging
from abc import ABC, abstractmethod
from pathlib import Path

import vlc

from music.metadata.now_playing import NowPlaying
from music.players.bases.base_player import BasePlayer

logger = logging.getLogger(f'weckpi.{__name__}')


class SingleMediaBasePlayer(BasePlayer, ABC):
    """
    The base for every vlc player for single media sources

    This class is an abstract class, do not instantiate it directly!
    """
    player: vlc.MediaPlayer
    media: vlc.Media
    mrl = str | Path

    def __init__(self, *args: str):
        """
        The base for every vlc player for single media sources

        :param args: Arguments to pass to vlc.
        For possible arguments, see the help of the vlc cli.
        """
        super().__init__(*args)
        self.player = self.instance.media_player_new()

    @abstractmethod
    def set_media(self, mrl: str | Path, now_playing: NowPlaying) -> None:
        """Set the media source"""

    def next(self) -> None:
        """Jump to the next item in the playlist (not supported)"""
        logger.warning('Next is not supported for single media types')

    def previous(self) -> None:
        """Jump to the previous item in the playlist (not supported)"""
        logger.warning('Previous is not supported for single media types')

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
