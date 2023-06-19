""""""
from __future__ import annotations

from dataclasses import dataclass

import weckpi.api.authentication as wpa


@dataclass(frozen=True)
class CodeAuthenticationResponse(wpa.AuthenticationResponse):
    """"""
    link: str
    code: str

    def __repr__(self) -> str:
        return f'Open {self.link} in your browser and enter the code {self.code}. The code expires in {self.expires}'
