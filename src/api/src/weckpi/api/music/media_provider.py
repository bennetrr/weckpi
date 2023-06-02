from __future__ import annotations

from abc import *
from pathlib import Path

import weckpi.api.music


class MediaProvider(ABC):
    """
    A music provider is the interface for accessing music resources that are saved on the disk,
    in the local network or somewhere in the internet.

    A music provider handles:

    - Authenticating to the provider
    - Searching / listing the available content
    - Getting a playable URI
    - Getting metadata like title, artist, album image, etc.
    """

    @abstractmethod
    def login(self, credential_file: Path):
        """Sign in at the provider."""

    @abstractmethod
    def search(self, search_term: str) -> NotImplemented:
        """Search the provider's available content for the search term."""

    @abstractmethod
    def explore(self, path: str = "/") -> NotImplemented:
        """List the provider's available content in the given path."""

    @abstractmethod
    def resolve_mrid(self, mrid: str) -> weckpi.api.music.MediaResource:
        """Get all the information of the given media resource like URI and metadata."""

    @abstractmethod
    def get_metadata(self, mrid: str) -> weckpi.api.music.Metadata:
        """Get the metadata of the given media resource."""

    # Flags to tell the core application what the provider is capable of
    @property
    @abstractmethod
    def needs_login(self) -> bool:
        """Whether the user needs to sign in to the provider."""

    @property
    @abstractmethod
    def can_explore(self) -> bool:
        """Whether the provider supports exploring."""

    @property
    @abstractmethod
    def can_search(self) -> bool:
        """Whether the provider supports searching."""
