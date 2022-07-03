"""A player for multiple media sources"""
from music.metadata.playlist_item import PlaylistItem
from music.players.bases.playlist_base_player import PlaylistBasePlayer
from music.tidal.tidal_session import TidalSession


class PlaylistPlayer(PlaylistBasePlayer):
    """A player for multiple media sources"""
    def __init__(self, playlist: list[PlaylistItem], *args: str, tidal_session: TidalSession = None):
        """
        A player for multiple media sources

        :param playlist: The items to initially put in the playlist
        :param args: Arguments to pass to vlc.
        For possible arguments, see the help of the vlc cli.
        :param tidal_session: A valid TIDAL session
        """
        super().__init__(playlist, *args, tidal_session=tidal_session)

    def set_playlist(self, items: list[PlaylistItem]) -> None:
        """Set the playlist"""
        was_playing = self.is_playing

        self.playlist = items

        if was_playing:
            self.play()

    def add_item(self, item: PlaylistItem) -> None:
        """Add an item to the playlist"""
        self.playlist.append(item)

    def add_items(self, items: list[PlaylistItem]) -> None:
        """Add a list of items to the playlist"""
        self.playlist.extend(items)
