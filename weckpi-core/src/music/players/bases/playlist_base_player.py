"""The base for every vlc player for multiple media sources"""
from abc import ABC, abstractmethod

import vlc

from music.metadata.playlist_item import PlaylistItem
from music.players.bases.base_player import BasePlayer


class PlaylistBasePlayer(BasePlayer, ABC):
    """
    The base for every vlc player for multiple media sources

    This class is an abstract class, do not instantiate it directly!
    """
    playlist: list[PlaylistItem]
    playlist_index: int

    def __init__(self, *args: str):
        """
        A player for a multiple media sources in a playlist

        :param args: Arguments to pass to vlc.
        For possible arguments, see vlc --help
        """
        super().__init__(*args)
        self.player = self.instance.media_list_player_new()
        event_manager: vlc.EventManager = self.player.event_manager()

        event_manager.event_attach(vlc.EventType.MediaPlayerStopped, self.stop_handler)

    @abstractmethod
    def set_playlist(self, items: list[PlaylistItem]) -> None:
        """Set the playlist"""
        self.playlist = items

    @abstractmethod
    def add_item(self, item: PlaylistItem) -> None:
        """Add an item to the playlist"""

    @abstractmethod
    def add_items(self, items: list[PlaylistItem]) -> None:
        """Add a list of items to the playlist"""

    def next(self) -> None:
        """Jump to the next item in the playlist"""

    def previous(self) -> None:
        """Jump to the previous item in the playlist"""

    # noinspection PyUnusedLocal
    def stop_handler(self, e: vlc.Event) -> None:  # pylint: disable=W0613
        """Event handler for vlc when the player is stopped"""

    @property
    def playlist_length(self) -> int:
        """Get the length of the playlist"""
        return len(self.playlist)

    def __str__(self):
        return f'{self.now_playing} [{self.playlist_index + 1} / {self.playlist_length}]'
