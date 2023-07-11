""""""
from __future__ import annotations

from concurrent.futures import Future
from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticationResponse:
    """"""
    succeeded: ...
    expires: ...


@dataclass
class OAuthCredentials:
    token_type: str
    access_token: str
    refresh_token: str
    expire_time: str
