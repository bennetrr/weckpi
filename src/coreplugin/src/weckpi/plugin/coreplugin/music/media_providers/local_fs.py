"""A media provider to play media files from the local filesystem."""
from __future__ import annotations

from pathlib import Path
from shutil import copy
from uuid import uuid4

import mutagen

from weckpi.api.music import MediaProvider, MediaResource, Metadata


# TODO Add unit tests


class LocalFS(MediaProvider):
    """
    A media provider to play media files from the local filesystem.

    The MRID format is ``localFs:localFs:/Path/To/Song.mp3``.
    A providerInstanceId other than the one shown above is not accepted!

    This media provider needs a folder in the static assets server,
    so that the album covers can be displayed in the web app.
    """
    _album_cover_dir: Path
    _available_covers: dict[Path, str]

    def __init__(self, album_cover_dir: Path):
        self._album_cover_dir = album_cover_dir
        self._album_cover_dir.mkdir(parents=True, exist_ok=True)
        self._available_covers = {}

    login = None

    search = None

    def explore(self, path: str = "/"):
        """List all media files and directories containing media files in the given path."""
        # TODO Implement
        raise NotImplementedError

    @staticmethod
    def _check_mrid(mrid: str) -> tuple[str, str, Path]:
        """Check if the given MRID is valid for this plugin instance."""
        provider_id, provider_instance_id, path_str = mrid.split(':', 2)

        if provider_id != 'localFs' or provider_instance_id != 'localFs':
            raise ValueError(
                f'Invalid MRID {mrid}: '
                f'The provider id and provider instance id both have to be "localFs", '
                f'but the given values are {provider_id} and {provider_instance_id}!'
            )

        path = Path(path_str)
        if not path.is_file():
            raise FileNotFoundError(
                f'Invalid MRID {mrid}:'
                f'The file {path} does not exist on the local filesystem!'
            )

        return provider_id, provider_instance_id, path

    def resolve_mrid(self, mrid: str):
        """Get all the information of the given media resource like URI and metadata."""
        _, _, path = self._check_mrid(mrid)

        return MediaResource(
            provider=self,
            mrid=mrid,
            uri=str(path),
            metadata=self.get_metadata(mrid),
            continuous=False
        )

    def get_metadata(self, mrid: str):
        """Get the metadata of the given media resource."""
        # TODO Implement metadata retrieving for more file types,
        #  maybe move this to the api, so other plugins can also use this
        _, _, path = self._check_mrid(mrid)

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
            image=f'http://localhost:5001/localFs/{server_name}',  # TODO Use dynamic URL from plugin manager
            duration=media_file.info.length / 60
        )
