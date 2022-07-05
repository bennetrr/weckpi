"""The base for every vlc player for multiple media sources"""
import logging
from abc import ABC, abstractmethod
from typing import Optional

import vlc

from music.metadata.now_playing import NowPlaying
from music.metadata.playlist_item import PlaylistItem
from music.players.bases.base_player import BasePlayer
from music.tidal.tidal_session import TidalSession
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
    tidal_session: TidalSession
    disable_stop_handler = False

    # Event handling
    media_player_stopped_triggered = False

    def __init__(self, playlist: list[PlaylistItem], *args: str, tidal_session: TidalSession = None):
        """
        A player for a multiple media sources in a playlist

        :param playlist: The items to initially put in the playlist
        :param args: Arguments to pass to vlc.
        For possible arguments, see vlc --help
        :param tidal_session: A valid TIDAL session
        """
        super().__init__(*args)
        self.tidal_session = tidal_session

        self.event_manager = self.player.event_manager()
        # noinspection PyUnresolvedReferences
        self.event_manager.event_attach(vlc.EventType.MediaPlayerStopped, self.media_player_stopped_handler)

        self.set_playlist(playlist)
        self.load_item()

    @abstractmethod
    def set_playlist(self, items: list[PlaylistItem]) -> None:
        """Set the playlist"""

    @abstractmethod
    def add_item(self, item: PlaylistItem) -> None:
        """Add an item to the playlist"""

    @abstractmethod
    def add_items(self, items: list[PlaylistItem]) -> None:
        """Add a list of items to the playlist"""

    def load_item(self) -> None:
        """Load the current item in the playlist"""
        mrl = get_mrl(self.playlist[self.playlist_index].uri, self.tidal_session)
        vlc_media = self.instance.media_new(mrl)
        self.player.set_media(vlc_media)

    def next(self) -> None:
        """Jump to the next item in the playlist"""
        # Check if we're not already at the end of the playlist
        if self.playlist_index + 1 >= len(self.playlist):
            logger.info('End of playlist reached!')
            return

        self.playlist_index += 1
        self.disable_stop_handler = True
        self.stop()
        self.load_item()
        self.play()
        self.disable_stop_handler = False

    def previous(self) -> None:
        """Jump to the previous item in the playlist"""
        # Check if we're not already at the beginning of the playlist
        if self.playlist_index - 1 <= 0:
            logger.info('Beginning of playlist reached!')
            return

        self.playlist_index -= 1
        self.disable_stop_handler = True
        self.stop()
        self.load_item()
        self.play()
        self.disable_stop_handler = False

    def jump_to(self, index: int) -> None:
        """Jump to a specific item in the playlist"""
        if index < 0 or index >= len(self.playlist):
            logger.error('Invalid index!')
            return

        self.playlist_index = index
        self.disable_stop_handler = True
        self.stop()
        self.load_item()
        self.play()
        self.disable_stop_handler = False

    def stop(self) -> None:
        """Stop the playback of the media and reset the media"""
        super().stop()
        self.set_playlist(self.playlist)

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

    # Event handling
    def event_loop(self) -> None:
        """Event loop for the player"""
        # MediaPlayerStopped
        if self.media_player_stopped_triggered:
            if not self.disable_stop_handler:
                self.next()
        self.media_player_stopped_triggered = False

    # noinspection PyUnusedLocal
    def media_player_stopped_handler(self, e: vlc.Event) -> None:  # pylint: disable=W0613
        """Event handler for when the track ended"""
        self.media_player_stopped_triggered = True
