"""A player for multiple media sources"""
from typing import Optional

from music.metadata.now_playing import NowPlaying
from music.metadata.playlist_item import PlaylistItem
from music.players.bases.playlist_base_player import PlaylistBasePlayer


class PlaylistPlayer(PlaylistBasePlayer):
    def __init__(self, items: list[PlaylistItem], *args: str):
        """
        A player for multiple media sources

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

        self.add_items(items)

        if was_playing:
            self.play()

    def add_item(self, item: PlaylistItem) -> None:
        """Add an item to the playlist"""
        self.playlist.add_media(item.mrl)
        self.playlist_items.append(item)

    def add_items(self, items: list[PlaylistItem]) -> None:
        """Add a list of items to the playlist"""
        for item in items:
            self.add_item(item)

    @property
    def now_playing(self) -> Optional[NowPlaying]:
        """Get information about the song that is playing now"""
        if not self.is_playing:
            return None

        current_song = self.playlist_items[self.playlist_index]
        return current_song.now_playing
