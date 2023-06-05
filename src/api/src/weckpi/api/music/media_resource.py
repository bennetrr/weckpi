from __future__ import annotations

from dataclasses import dataclass

import weckpi.api.music as wpm


@dataclass(init=True, )
class MediaResource:
    """"""
    provider: wpm.MediaProvider
    mrid: str
    uri: str
    metadata: wpm.Metadata
