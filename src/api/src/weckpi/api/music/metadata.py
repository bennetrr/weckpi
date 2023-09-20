"""The model of the metadata of a media resource."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Metadata:
    """
    The model of the metadata of a media resource.

    :var title: The title of the media resource.
    :var artist: The artist of the media resource.
    :var album: The album that the media resource is released on.
    :var image: URI of an image, for example the album cover or the logo of the internet radio station.
    :var duration: The duration of the media resource in minutes.
    """
    title: str
    artist: str
    album: str
    image: str | None
    duration: float
