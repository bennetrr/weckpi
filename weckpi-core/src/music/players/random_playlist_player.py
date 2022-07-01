"""A player for multiple media sources in random order"""
from typing import Optional
from random import shuffle, randint

from music.metadata.now_playing import NowPlaying
from music.metadata.playlist_item import PlaylistItem
from music.players.bases.playlist_base_player import PlaylistBasePlayer


class RandomPlaylistPlayer(PlaylistBasePlayer):
    """A player for multiple media sources in random order"""
    def __init__(self, items: list[PlaylistItem], *args: str):
        """
        A player for multiple media sources in random order

        :param items: The items to initially put in the playlist
        :param args: Arguments to pass to vlc.
        For possible arguments, see the help of the vlc cli.
        """
        super().__init__(*args)
        self.set_playlist(items)

    def set_playlist(self, items: list[PlaylistItem]) -> None:
        """Set the playlist"""
        was_playing = self.is_playing

        self.playlist = self.instance.media_list_new()
        self.player.set_media_list(self.playlist)
        self.playlist_items = []

        shuffle(items)

        for item in items:
            self.playlist.add_media(item.mrl)
            self.playlist_items.append(item)

        if was_playing:
            self.play()

    def add_item(self, item: PlaylistItem) -> None:
        """Add an item to the playlist"""
        if self.playlist_index < 0:
            playlist_index = 0
        else:
            playlist_index = self.playlist_index

        index = randint(playlist_index, self.playlist.count())
        self.playlist.insert_media(item.mrl, index)
        self.playlist_items.insert(index, item)

    def add_items(self, items: list[PlaylistItem]) -> None:
        """Add a list of items to the playlist"""
        for item in items:
            self.add_item(item)

    def stop(self) -> None:
        """Stop the playback of the media and reset the media"""
        super().stop()
        self.set_playlist(self.playlist_items)
