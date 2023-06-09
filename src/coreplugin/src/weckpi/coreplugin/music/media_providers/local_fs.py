"""Media Provider to play media files from the local filesystem."""
from __future__ import annotations

from pathlib import Path

import mutagen

from weckpi.api.music import MediaProvider, MRID, Metadata, MediaResource


class LocalFS(MediaProvider):
    """
    Media Provider to play media files from the local filesystem.

    The MRID format is local-fs:local-fs:/path/to/media/file.mp3
    """
    def login(self, credential_file: Path):
        """
        No login needed for this media provider.

        :raises NotImplementedError:
        """
        raise NotImplementedError

    def search(self, search_term: str):
        """
        Searching is not available for this media provider.

        :raises NotImplementedError:
        """
        raise NotImplementedError

    def explore(self, path: str = "/") -> NotImplemented:
        """List all media files and directories containing media files in the given path."""
        return NotImplemented

    def resolve_mrid(self, mrid: MRID) -> MediaResource:
        provider_id, provider_instance_id, path_str = mrid.split(':', 2)

        if provider_id != 'local-fs' or provider_instance_id != 'local-fs':
            raise ValueError(f'Invalid MRID {mrid}: '
                             f'The provider id and provider instance id both have to be "local-fs", '
                             f'but the given values are {provider_id} and {provider_instance_id}!')

        path = Path(path_str)
        if not path.is_file():
            raise FileNotFoundError(f'Invalid MRID {mrid}:'
                                    f'The file {path} does not exist on the local filesystem!')

        media_file = mutagen.File(path, easy=True)
        return MediaResource(
            provider=self,
            mrid=mrid,
            uri=str(path),
            metadata=Metadata(
                title=media_file['Title'][0].value,
                artist=media_file['Author'][0].value,
                album=media_file['WM/AlbumTitle'][0].value,
                image='',
                played_from='This WeckPi'
            ),
            continuous=False
        )

    def get_metadata(self, mrid: MRID) -> Metadata:
        return Metadata('', '', '', '', '')
