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
    player: vlc.MediaListPlayer
    playlist: vlc.MediaList
    playlist_items: list[PlaylistItem]
    playlist_index = -1

    def __init__(self, *args: str):
        """
        A player for a multiple media sources in a playlist

        :param args: Arguments to pass to vlc.
        For possible arguments, see the help of the vlc cli.
        """
        super().__init__(*args)
        self.player = self.instance.media_list_player_new()
        event_manager: vlc.EventManager = self.player.get_media_player().event_manager()

        event_manager.event_attach(vlc.EventType.MediaPlayerMediaChanged, self.next_song_handler)
        event_manager.event_attach(vlc.EventType.MediaPlayerStopped, self.stop_handler)

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
        self.player.next()

    def previous(self) -> None:
        """Jump to the previous item in the playlist"""
        self.player.previous()
        self.playlist_index -= 2

    # noinspection PyUnusedLocal
    def next_song_handler(self, e: vlc.Event) -> None:  # pylint: disable=W0613
        """Event handler for vlc when a song is ending"""
        self.playlist_index += 1

    # noinspection PyUnusedLocal
    def stop_handler(self, e: vlc.Event) -> None:  # pylint: disable=W0613
        """Event handler for vlc when the player is stopped"""
        self.playlist_index = -1

    @property
    def volume(self) -> int:
        """Get the volume of the player"""
        return self.player.get_media_player().audio_get_volume()

    @volume.setter
    def volume(self, volume) -> None:
        """
        Set the volume of the player

        :param volume: The volume in percent (0 = mute, 100 = 0dB)
        :raises ValueError: If the given volume is out of range
        """
        if volume < 0 or volume > 100:
            raise ValueError(f'The volume is out of range (0≰{volume}≰100)')
        self.player.get_media_player().audio_set_volume(volume)

    @property
    def playlist_length(self) -> int:
        """Get the length of the playlist"""
        return self.playlist.count()

    def __str__(self):
        return f'{self.now_playing} [{self.playlist_index + 1} / {self.playlist_length}]'
