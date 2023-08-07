"""Model for the result of the authentication."""
from __future__ import annotations

from dataclasses import dataclass

import weckpi.api.authentication as wpa


@dataclass(frozen=True)
class AuthenticationResult:
    """
    Model for the result of the authentication.

    :var successful: If the authentication was successful.
    :var auth_session: If ``successful == True``, the session details, so that the session can be loaded another time.
    """
    successful: bool
    auth_session: wpa.OAuthSession | None = None
