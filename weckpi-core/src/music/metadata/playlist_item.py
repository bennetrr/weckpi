"""A model for an item of a playlist"""
from dataclasses import dataclass
from pathlib import Path

from music.metadata.now_playing import NowPlaying


@dataclass
class PlaylistItem:
    """A model for an item of a playlist"""
    uri: str | Path
    now_playing: NowPlaying
