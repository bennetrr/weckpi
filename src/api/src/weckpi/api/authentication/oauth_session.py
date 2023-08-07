"""A model for a saved OAuth session."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class OAuthSession:
    """
    A model for a saved OAuth session.

    :var token_type: The type of the token, e.g. ``Bearer``.
    :var access_token: The token used to authenticate to the service.
    :var refresh_token: The token used to renew the access token when it expires.
    :var expire_time: The time when the access token expires.
    """
    token_type: str
    access_token: str
    refresh_token: str
    expire_time: datetime
