"""A player for multiple media sources"""
from pathlib import Path
from typing import Optional

import vlc

from music.metadata import NowPlaying
from music.players.bases.playlist_base_player import PlaylistBasePlayer


class PlaylistPlayer(PlaylistBasePlayer):
    def __init__(self, media_sources: dict[str | Path, NowPlaying], *args: str):
        """
        A player for multiple media sources

        :param media_sources:
        :param args: Arguments to pass to vlc.
        For possible arguments, see the help of the vlc cli.
        """
        super().__init__(*args)
        self.player = self.instance.media_player_new()
        self.set_playlist(media_sources)

    def set_playlist(self, media_sources: dict[str | Path, NowPlaying]) -> None:
        """Set the playlist"""
        was_playing = self.is_playing

        self.playlist = self.instance.media_list_new()
        self.player.set_media_list(self.playlist)

        for media_source in media_sources:
            self.playlist.add_media(media_source)

        self.media_sources = media_sources
        if was_playing:
            self.play()

    def add_source_to_playlist(self, media_source: str | Path, now_playing: NowPlaying) -> None:
        """Add a source to the playlist"""
        self.playlist.add_media(media_source)
        self.media_sources[media_source] = now_playing

    def next(self) -> None:
        """Jump to the next item in the playlist"""
        self.player.next()

    def previous(self) -> None:
        """Jump to the previous item in the playlist"""
        self.player.previous()

    @property
    def now_playing(self) -> Optional[NowPlaying]:
        """Get information about the song that is playing now"""
        if not self.is_playing:
            return None
