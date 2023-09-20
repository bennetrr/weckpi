"""Models for responses from services that contain information on how to authenticate to the service."""
from __future__ import annotations

from concurrent.futures import Future
from dataclasses import dataclass
from datetime import datetime

import weckpi.api.authentication as wpa


@dataclass(frozen=True)
class AuthenticationDetails:
    """
    Base model of the information needed to authenticate to a service.

    **DO NOT INSTANTIATE THIS CLASS DIRECTLY!**

    :var result: If the authentication was successful, and the session details if available.
    :var expires: The time when the login link etc. gets invalid.
    """
    result: Future[wpa.AuthenticationResult]
    expires: datetime


@dataclass(frozen=True)
class CodeAuthenticationDetails(AuthenticationDetails):
    """
    Model of the information needed to authenticate using a code that needs to be entered into a website.

    :var code: The code that identifies this session.
    :var link: A link to a website where the code has to be entered.
    """
    code: str
    link: str

    def __repr__(self):
        return f'Open {self.link} in your browser and enter the code {self.code}. The code expires in {self.expires}'


@dataclass(frozen=True)
class LinkAuthenticationDetails(AuthenticationDetails):
    """
    Model of the information needed to authenticate using a link.

    :var link: A link with a token / code that is used to authenticate.
    """
    link: str

    def __repr__(self):
        return f'Open {self.link} in your browser. The link expires in {self.expires}'
