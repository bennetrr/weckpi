from __future__ import annotations

from abc import *
from pathlib import Path

import weckpi.api.music as wpm


class MediaProvider(ABC):
    """
    Interface for all media providers.

    A media provider class contains the code for accessing media resources that are saved on the disk,
    in the local network or somewhere on the internet.

    A media provider handles:

    - Authenticating to the provider
    - Searching / listing the available content
    - Getting a playable URI
    - Getting metadata like title, artist, album image, etc.

    MRID: provider_id:provider_instance_id:provider_specific_id

    Examples:

    - tidal:my-user:song-from-artist
    - local-fs:local-fs:/mnt/daten/Music/Path/To/Song.mp3
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
    def resolve_mrid(self, mrid: str) -> wpm.MediaResource:
        """Get all the information of the given media resource like URI and metadata."""

    @abstractmethod
    def get_metadata(self, mrid: str) -> wpm.Metadata:
        """Get the metadata of the given media resource."""
