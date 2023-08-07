"""Base class for all media providers."""
from __future__ import annotations

from abc import ABC, abstractmethod

import weckpi.api.music as wpm
from weckpi.api.authentication import AuthenticationDetails, AuthenticationResult, OAuthSession


class MediaProvider(ABC):
    """
    Base Class for all media providers.

    A media provider class contains the code for accessing media resources that are saved on the disk,
    in the local network or somewhere on the internet.

    A media provider handles:

    - Authenticating to the provider
    - Searching / listing the available content
    - Getting a playable URI
    - Getting metadata like title, artist, album image, etc.

    The MRID format (media resource ID) is used for exchanging and saving media resources.
    It's a simple string in the format ``providerId:providerInstanceId:providerSpecificId``.
    Every part should be in camelCase (if possible) and seperated by a colon (``:``).
    For the ``providerSpecificId``, colons are allowed, since only the first two are used for separation.

    Examples:

    - ``tidal:myUser:songFromArtist``
    - ``localFs:localFs:/mnt/daten/Music/Path/To/Song.mp3``
    """

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def login(self, auth_session: OAuthSession) -> AuthenticationResult | list[AuthenticationDetails]:
        """Log in to the provider."""

    @abstractmethod
    def search(self, search_term: str) -> list[wpm.SearchResult]:
        """Search the provider's available content for the search term."""

    @abstractmethod
    def explore(self, mrid: str) -> list[wpm.SearchResult]:
        """List the provider's available content in the given path."""

    @abstractmethod
    def resolve_mrid(self, mrid: str) -> wpm.MediaResource:
        """Get all the information of the given media resource like URI and metadata."""

    @abstractmethod
    def get_metadata(self, mrid: str) -> wpm.Metadata:
        """Get the metadata of the given media resource."""
