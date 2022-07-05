"""A player for multiple media sources in random order"""
from random import shuffle, randint

from music.metadata.playlist_item import PlaylistItem
from music.players.bases.playlist_base_player import PlaylistBasePlayer


class RandomPlaylistPlayer(PlaylistBasePlayer):
    """A player for multiple media sources in random order"""
    def set_playlist(self, items: list[PlaylistItem]) -> None:
        """Set the playlist"""
        was_playing = self.is_playing

        shuffle(items)
        self.playlist = items

        if was_playing:
            self.load_item()
            self.play()

    def add_item(self, item: PlaylistItem) -> None:
        """Add an item to the playlist"""
        if self.playlist_index < 0:
            playlist_index = 0
        else:
            playlist_index = self.playlist_index

        index = randint(playlist_index, len(self.playlist))
        self.playlist.insert(index, item)

    def add_items(self, items: list[PlaylistItem]) -> None:
        """Add a list of items to the playlist"""
        for item in items:
            self.add_item(item)
