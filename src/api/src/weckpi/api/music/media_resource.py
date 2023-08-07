"""The model of the information required to play a media resource."""
from __future__ import annotations

from dataclasses import dataclass

import weckpi.api.music as wpm


@dataclass(frozen=True)
class MediaResource:
    """
    The model of the information required to play a media resource.

    :var provider: The provider instance from which this media resource is.
    :var mrid: The MRID.
    :var uri: The playable URI of the media resource. Can be a URL to a webserver or to the local file system.
    :var metadata: The metadata of the media resource.
                   When ``continuous`` is ``True``, ``provider.getMetadata()`` is used instead,
                   because the data is suspected to change. This may still be used as a backup.
    :var continuous: Whether the media ressource is continuous (should be ``true`` for internet radio and similar).
    """
    provider: wpm.MediaProvider
    mrid: str
    uri: str
    metadata: wpm.Metadata
    continuous: bool


class MediaNotAvailableException(RuntimeError):
    """An exception that tells the media player that the requested resource is not available."""
