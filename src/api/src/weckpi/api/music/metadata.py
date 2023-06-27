from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Metadata:
    """
    The metadata of a media resource:

    - Title
    - Artist
    - Album
    - An image that could be the album cover, the image of an internet radio station or playlist, etc.
    - The name of the provider, playlist, radio station, etc.
    """
    title: str
    artist: str
    album: str
    image: str | None

    def __repr__(self):
        return f'{self.artist} - {self.title} from {self.album}'
