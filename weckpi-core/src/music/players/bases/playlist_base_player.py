"""The base for every vlc player for multiple media sources"""
from abc import ABC, abstractmethod
from pathlib import Path

import vlc

from music.metadata import NowPlaying
from music.players.bases.base_player import BasePlayer


class PlaylistBasePlayer(BasePlayer, ABC):
    """
    The base for every vlc player for multiple media sources

    This class is an abstract class, do not instantiate it directly!
    """
    player: vlc.MediaListPlayer
    playlist: vlc.MediaList
    media_sources: dict[str | Path, NowPlaying]

    def __init__(self, *args: str):
        """
        A player for a multiple media sources in a playlist

        :param args: Arguments to pass to vlc.
        For possible arguments, see the help of the vlc cli.
        """
        super().__init__(*args)
        self.player = self.instance.media_player_new()
        event_manager: vlc.EventManager = self.player.event_manager
        event_manager.event_attach(vlc.EventType, self.on_next_song)
        # https://www.olivieraubert.net/vlc/python-ctypes/doc/

    @abstractmethod
    def set_playlist(self, media_sources: dict[str | Path, NowPlaying]) -> None:
        """Set the playlist"""

    @abstractmethod
    def add_source_to_playlist(self, media_source: str | Path, now_playing: NowPlaying) -> None:
        """Add a source to the playlist"""

    def next(self) -> None:
        """Jump to the next item in the playlist"""
        self.player.next()

    def previous(self) -> None:
        """Jump to the previous item in the playlist"""
        self.player.previous()

    def on_next_song(self, e: vlc.Event) -> None:
        """Event handler for vlc when a song is ending"""
        self.playlist_index += 1
