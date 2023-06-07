from __future__ import annotations

from dataclasses import dataclass
from typing import NewType

import weckpi.api.music as wpm

MRID = NewType('MRID', str)


@dataclass(kw_only=True, frozen=True)
class MediaResource:
    """"""
    provider: wpm.MediaProvider
    mrid: MRID
    uri: str
    metadata: wpm.Metadata
    continuous: bool
