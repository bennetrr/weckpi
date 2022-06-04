"""Tools for working with metadata for the song that is playing now"""
from dataclasses import dataclass


@dataclass
class NowPlaying:
    """Information about the song that is playing now"""
    title: str
    artist: str
    album: str
    cover: str

    def __str__(self):
        """Return the now playing information as a string"""
        return f'{self.artist} - {self.title} (from {self.album})'
