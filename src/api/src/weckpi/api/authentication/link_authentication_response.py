""""""
from __future__ import annotations

from dataclasses import dataclass

import weckpi.api.authentication as wpa


@dataclass(frozen=True)
class LinkAuthenticationResponse(wpa.AuthenticationResponse):
    """"""
    link: str

    def __repr__(self) -> str:
        return f'Open {self.link} in your browser. The link expires in {self.expires}'
