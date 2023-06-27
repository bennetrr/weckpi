from __future__ import annotations

from dataclasses import dataclass

import weckpi.api.music as wpm


@dataclass(kw_only=True, frozen=True)
class MediaResource:
    """"""
    provider: wpm.MediaProvider
    mrid: str
    uri: str
    metadata: wpm.Metadata
    continuous: bool
