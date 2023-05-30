from __future__ import annotations

from dataclasses import dataclass

from weckpi.api.music import MediaProvider, Metadata


@dataclass(init=True, )
class MediaResource:
    """"""
    provider: MediaProvider
    mrid: str
    uri: str
    metadata: Metadata
