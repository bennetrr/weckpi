"""The base for every vlc player for multiple media sources"""
import logging
from abc import ABC, abstractmethod
from typing import Optional

import vlc

from music.metadata.now_playing import NowPlaying
from music.metadata.playlist_item import PlaylistItem
from music.players.bases.base_player import BasePlayer
from utils.music import get_mrl

logger = logging.getLogger(f'weckpi.{__name__}')


class PlaylistBasePlayer(BasePlayer, ABC):
    """
    The base for every vlc player for multiple media sources

    This class is an abstract class, do not instantiate it directly!
    """
    playlist: list[PlaylistItem] = []
    playlist_index: int = 0
    event_manager: vlc.EventManager

    def __init__(self, *args: str):
        """
        A player for a multiple media sources in a playlist

        :param args: Arguments to pass to vlc.
        For possible arguments, see vlc --help
        """
        super().__init__(*args)

        self.event_manager = self.player.event_manager()
        self.event_manager.event_attach(vlc.EventType.MediaPlayerStopped, self.stop_handler)

        self.next()

    @abstractmethod
    def set_playlist(self, items: list[PlaylistItem]) -> None:
        """Set the playlist"""

    @abstractmethod
    def add_item(self, item: PlaylistItem) -> None:
        """Add an item to the playlist"""

    @abstractmethod
    def add_items(self, items: list[PlaylistItem]) -> None:
        """Add a list of items to the playlist"""

    def next(self) -> None:
        """Jump to the next item in the playlist"""
        # Check if we're not already at the end of the playlist
        if len(self.playlist) >= self.playlist_index + 1:
            logger.info('End of playlist reached!')
            return

        self.playlist_index += 1
        mrl = get_mrl(self.playlist[self.playlist_index].mrl)
        vlc_media = self.instance.media_new(mrl)
        self.player.set_media(vlc_media)
        self.player.play()

    def previous(self) -> None:
        """Jump to the previous item in the playlist"""

    # noinspection PyUnusedLocal
    def stop_handler(self, e: vlc.Event) -> None:  # pylint: disable=W0613
        """Event handler for vlc when the player is stopped"""
        self.next()

    @property
    def playlist_length(self) -> int:
        """Get the length of the playlist"""
        return len(self.playlist)

    @property
    def now_playing(self) -> Optional[NowPlaying]:
        """Get information about the song that is playing now"""
        if not self.is_playing:
            return None

        current_song = self.playlist[self.playlist_index]
        return current_song.now_playing

    def __str__(self):
        return f'{self.now_playing} [{self.playlist_index + 1} / {self.playlist_length}]'
