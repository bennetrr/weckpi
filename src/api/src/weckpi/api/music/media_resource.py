from __future__ import annotations

from dataclasses import dataclass
from typing import NewType

import weckpi.api.music as wpm

MRID = NewType('MRID', str)


@dataclass(init=True)
class MediaResource:
    """"""
    provider: wpm.MediaProvider
    mrid: MRID
    uri: str
    metadata: wpm.Metadata
    continuous: bool
