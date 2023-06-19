""""""
from __future__ import annotations

from concurrent.futures import Future
from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticationResponse:
    """"""
    succeeded: ...
    expires: ...
