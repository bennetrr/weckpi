"""The base for every vlc player for single media sources"""
import logging
from abc import ABC, abstractmethod

import vlc

from music.metadata.now_playing import NowPlaying
from music.players.bases.base_player import BasePlayer

logger = logging.getLogger(f'weckpi.{__name__}')


class SingleMediaBasePlayer(BasePlayer, ABC):
    """
    The base for every vlc player for single media sources

    This class is an abstract class, do not instantiate it directly!
    """
    media: vlc.Media
    mrl = str

    @abstractmethod
    def set_media(self, mrl: str, now_playing: NowPlaying) -> None:
        """Set the media source"""

    def next(self) -> None:
        """Jump to the next item in the playlist (not supported)"""
        logger.warning('Next is not supported for single media types')

    def previous(self) -> None:
        """Jump to the previous item in the playlist (not supported)"""
        logger.warning('Previous is not supported for single media types')
