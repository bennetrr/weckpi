"""Tools for fetching metadata of internet radios"""
from dataclasses import dataclass


@dataclass
class NowPlaying:
    """Information about what song is playing now"""
    title: str
    artist: str
    album: str
    cover: str
