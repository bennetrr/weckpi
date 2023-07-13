"""Media Provider to play media files from the local filesystem."""
from __future__ import annotations

from pathlib import Path
from shutil import copy
from uuid import uuid4

import mutagen

from weckpi.api.music import MediaProvider, MediaResource, Metadata


class LocalFS(MediaProvider):
    """
    Media Provider to play media files from the local filesystem.

    The MRID format is local-fs:local-fs:/path/to/media/file.mp3
    """
    _album_cover_dir: Path
    _available_covers: dict[Path, str]

    def __init__(self, album_cover_dir: Path):
        self._album_cover_dir = album_cover_dir
        self._album_cover_dir.mkdir(parents=True)
        self._available_covers = {}

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

    def _check_mrid(self, mrid: str):
        """Check if the given MRID is valid for this plugin instance."""
        provider_id, provider_instance_id, path_str = mrid.split(':', 2)

        if provider_id != 'local-fs' or provider_instance_id != 'local-fs':
            raise ValueError(f'Invalid MRID {mrid}: '
                             f'The provider id and provider instance id both have to be "local-fs", '
                             f'but the given values are {provider_id} and {provider_instance_id}!')

        path = Path(path_str)
        if not path.is_file():
            raise FileNotFoundError(f'Invalid MRID {mrid}:'
                                    f'The file {path} does not exist on the local filesystem!')

    def resolve_mrid(self, mrid: str) -> MediaResource:
        path = Path(mrid.split(':', 2)[2])

        return MediaResource(
            provider=self,
            mrid=mrid,
            uri=str(path),
            metadata=self.get_metadata(mrid),
            continuous=False
        )

    def get_metadata(self, mrid: str) -> Metadata:
        self._check_mrid(mrid)

        path = Path(mrid.split(':', 2)[2])
        media_file = mutagen.File(path, easy=True)

        image_path = path.parent / 'Folder.jpg'
        server_name = self._available_covers.get(image_path)

        if server_name is None:
            server_name = f'{uuid4()}.jpg'
            copy(image_path, self._album_cover_dir / server_name)
            self._available_covers[image_path] = server_name

        return Metadata(
            title=media_file['Title'][0].value,
            artist=media_file['Author'][0].value,
            album=media_file['WM/AlbumTitle'][0].value,
            image=f'http://localhost:5001/local-fs/{server_name}',  # TODO make dynamic
            duration=media_file.info.length / 60
        )
