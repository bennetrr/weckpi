from __future__ import annotations

from dataclasses import dataclass

import weckpi.api.music


@dataclass(init=True, )
class MediaResource:
    """"""
    provider: weckpi.api.music.MediaProvider
    mrid: str
    uri: str
    metadata: weckpi.api.music.Metadata
