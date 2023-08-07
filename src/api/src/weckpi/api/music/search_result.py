"""Model of a search result."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SearchResult:
    """
    Model of a search result.

    :var mrid: The MRID of the resource / folder.
    :var is_media_resource: Whether the result is a playable media resource of a folder that contains resources.
    :var name: The display name of the resource / folder.
    :var image: URI of an image, for example the album cover or the logo of the internet radio station.
    :var text: Other information that are displayed below the name.
    """
    mrid: str
    is_media_resource: bool
    name: str
    image: str
    text: str = ''
