"""The base for every vlc player for multiple media sources"""
from abc import ABC, abstractmethod

import vlc

from music.metadata import PlaylistItem
from music.players.bases.base_player import BasePlayer


class PlaylistBasePlayer(BasePlayer, ABC):
    """
    The base for every vlc player for multiple media sources

    This class is an abstract class, do not instantiate it directly!
    """
    player: vlc.MediaListPlayer
    playlist: vlc.MediaList
    playlist_items: list[PlaylistItem]
    playlist_index = 0

    def __init__(self, *args: str):
        """
        A player for a multiple media sources in a playlist

        :param args: Arguments to pass to vlc.
        For possible arguments, see the help of the vlc cli.
        """
        super().__init__(*args)
        self.player = self.instance.media_player_new()
        event_manager: vlc.EventManager = self.player.event_manager
        event_manager.event_attach(vlc.EventType.MediaListPlayerNextItemSet, self.next_song_handler)

    @abstractmethod
    def set_playlist(self, items: list[PlaylistItem]) -> None:
        """Set the playlist"""

    @abstractmethod
    def add_items(self, item: list[PlaylistItem]) -> None:
        """Add an item to the playlist"""

    def next(self) -> None:
        """Jump to the next item in the playlist"""
        self.player.next()

    def previous(self) -> None:
        """Jump to the previous item in the playlist"""
        self.player.previous()

    def next_song_handler(self, e: vlc.Event) -> None:
        """Event handler for vlc when a song is ending"""
        self.playlist_index += 1
