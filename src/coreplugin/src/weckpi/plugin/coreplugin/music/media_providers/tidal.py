"""Media provider for the streaming service TIDAL that uses the package `tidalapi <https://tidalapi.netlify.app/>`_."""
from __future__ import annotations

import logging
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Literal

import math
import tidalapi as tidal

from weckpi.api.authentication import AuthenticationResult, CodeAuthenticationDetails, LinkAuthenticationDetails, \
    OAuthSession
from weckpi.api.music import MediaNotAvailableException, MediaProvider, MediaResource, Metadata, SearchResult
from weckpi.api.utilities import flatten_dict

logger = logging.getLogger(__name__)

MediaTypes = Literal['album', 'artist', 'track', 'video', 'playlist']
TidalObjects = tidal.Artist | tidal.Album | tidal.Track | tidal.Video | tidal.Playlist


class Tidal(MediaProvider):
    """Media provider for the streaming service TIDAL."""
    _session: tidal.Session
    _instance_id: str

    def __init__(self, instance_id: str):
        session_config = tidal.Config()
        self._session = tidal.Session(session_config)
        self._instance_id = instance_id

    def login(self, auth_session: OAuthSession | None):
        """Log in to this instance with your TIDAL account, using a saved session if possible."""
        if auth_session is not None:
            logger.debug('Trying login with saved session')

            restore_success = self._session.load_oauth_session(
                auth_session.token_type,
                auth_session.access_token,
                auth_session.refresh_token,
                auth_session.expire_time
            )

            if restore_success:
                logger.info('Logged in from saved session')

                return AuthenticationResult(
                    successful=True,
                    auth_session=OAuthSession(
                        self._session.token_type,
                        self._session.access_token,
                        self._session.refresh_token,
                        self._session.expiry_time
                    )
                )

        logger.debug('Login with saved session was not successful, authentication by user needed')

        login, future = self._session.login_oauth()
        executor = ThreadPoolExecutor()
        promise = executor.submit(self._login, future)

        logger.info('Requested authentication by the user')

        return (CodeAuthenticationDetails(promise, login.expires_in, login.verification_uri, login.user_code),
                LinkAuthenticationDetails(promise, login.expires_in, login.verification_uri_complete))

    def _login(self, promise: Future) -> AuthenticationResult:
        """Second step of login."""
        promise.result()

        if not self._session.check_login():
            logger.info('Login was not successful')
            return AuthenticationResult(successful=False)

        logger.info('Login was successful')

        return AuthenticationResult(
            successful=True,
            auth_session=OAuthSession(
                self._session.token_type,
                self._session.access_token,
                self._session.refresh_token,
                self._session.expiry_time
            )
        )

    def _get_image(self, tidal_obj: TidalObjects) -> str | None:
        """Get the image from the TIDAL object. If no image is found, ``None`` is returned."""
        try:
            if isinstance(tidal_obj, tidal.Artist):
                return tidal_obj.image(750)
            if isinstance(tidal_obj, tidal.Album):
                return tidal_obj.image(1280)
            if isinstance(tidal_obj, tidal.Track):
                return self._get_image(tidal_obj.album)
            if isinstance(tidal_obj, tidal.Video):
                return self._get_image(tidal_obj.album)
            if isinstance(tidal_obj, tidal.Playlist):
                return tidal_obj.image(1080)
            raise TypeError(f'Object of class {tidal_obj.__class__.__name__} is not a valid TIDAL type!')
        except (AttributeError, ValueError) as exc:
            if isinstance(exc, AttributeError):  # TODO Temporary, fixed in upcoming release
                return None

            if exc.args[0] == 'No image available':
                return None
            raise exc

    def _to_search_result(self, tidal_obj: TidalObjects) -> SearchResult:
        """Convert a TIDAL object into a search result."""
        if isinstance(tidal_obj, tidal.Artist):
            return SearchResult(
                mrid=f'tidal:{self._instance_id}:artist:{tidal_obj.id}',
                is_media_resource=False,
                name=tidal_obj.name,
                image=self._get_image(tidal_obj)
            )
        if isinstance(tidal_obj, tidal.Album):
            return SearchResult(
                mrid=f'tidal:{self._instance_id}:album:{tidal_obj.id}',
                is_media_resource=False,
                name=tidal_obj.name,
                text=f'Album von {tidal_obj.artist.name}',  # TODO Localization
                image=self._get_image(tidal_obj)
            )
        if isinstance(tidal_obj, tidal.Track):
            return SearchResult(
                mrid=f'tidal:{self._instance_id}:track:{tidal_obj.id}',
                is_media_resource=True,
                name=tidal_obj.name,
                text=f'Song von {tidal_obj.artist.name}',  # TODO Localization
                image=self._get_image(tidal_obj)
            )
        if isinstance(tidal_obj, tidal.Video):
            return SearchResult(
                mrid=f'tidal:{self._instance_id}:video:{tidal_obj.id}',
                is_media_resource=True,
                name=tidal_obj.name,
                text=f'Video von {tidal_obj.artist.name}',  # TODO Localization
                image=self._get_image(tidal_obj)
            )
        if isinstance(tidal_obj, tidal.Playlist):
            return SearchResult(
                mrid=f'tidal:{self._instance_id}:playlist:{tidal_obj.id}',
                is_media_resource=False,
                name=tidal_obj.name,
                text=f'Playlist{f" von {tidal_obj.creator.name}" if tidal_obj.creator else ""}',  # TODO Localization
                image=self._get_image(tidal_obj)
            )
        raise TypeError(f'Object of class {tidal_obj.__class__.__name__} is not a valid TIDAL type!')

    def search(self, search_term: str):
        """Search TIDAL for the search term."""
        results: dict[str, TidalObjects] = self._session.search(search_term)
        del results['top_hit']
        flat_results = flatten_dict(results)
        return [self._to_search_result(res) for res in flat_results]

    def explore(self, mrid: str = None):
        """
        List the content that is available under the given MRID.

        :param mrid: Must be the MRID of type ``artist``, ``album`` or ``playlist``.
                     If omitted or ``None``, the "My ..." elements are returned.
        """
        if mrid is None:
            mrid = f'tidal:{self._instance_id}:library:overview'

        _, _, tidal_type, tidal_id = self._check_mrid(mrid)

        if tidal_type == 'library':
            if tidal_id == 'overview':
                return [
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:library:playlists',
                        is_media_resource=False,
                        name='Playlists',  # TODO Localization
                        image=None  # TODO Image
                    ),
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:library:artists',
                        is_media_resource=False,
                        name='Künstler',  # TODO Localization
                        image=None  # TODO Image
                    ),
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:library:albums',
                        is_media_resource=False,
                        name='Alben',  # TODO Localization
                        image=None  # TODO Image
                    ),
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:library:tracks',
                        is_media_resource=False,
                        name='Songs',  # TODO Localization
                        image=None  # TODO Image
                    ),
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:library:videos',
                        is_media_resource=False,
                        name='Videos',  # TODO Localization
                        image=None  # TODO Image
                    ),
                ]
            if tidal_id == 'artists':
                artists: list[tidal.Artist] = self._session.user.favorites.artists()
                return [self._to_search_result(x) for x in artists]
            if tidal_id == 'albums':
                albums: list[tidal.Album] = self._session.user.favorites.albums()
                return [self._to_search_result(x) for x in albums]
            if tidal_id == 'tracks':
                tracks: list[tidal.Track] = self._session.user.favorites.tracks()
                return [self._to_search_result(x) for x in tracks]
            if tidal_id == 'videos':
                videos: list[tidal.Video] = self._session.user.favorites.videos()
                return [self._to_search_result(x) for x in videos]
            if tidal_id == 'playlists':
                playlists = [*self._session.user.playlists(), *self._session.user.favorites.playlists()]
                return [self._to_search_result(x) for x in playlists]
            raise ValueError(f'TIDAL type library:{tidal_id} is not a valid type!')
        if tidal_type == 'artist':
            if tidal_id.endswith(':allTracks'):
                return [self._to_search_result(x)
                        for x in self._session.artist(tidal_id.removesuffix(':allTracks')).get_top_tracks()]

            tidal_obj = self._session.artist(tidal_id)

            albums: list[tidal.Album] = [
                *tidal_obj.get_albums(),
                *tidal_obj.get_albums_ep_singles(),
                *tidal_obj.get_albums_other()
            ]

            result: list[SearchResult] = [
                SearchResult(
                    mrid=f'{mrid}:allTracks',
                    is_media_resource=False,
                    name='Alle Songs',  # TODO Localization
                    image=self._get_image(tidal_obj)
                )
            ]

            result.extend([self._to_search_result(x) for x in albums])
            return result
        if tidal_type == 'album':
            tidal_obj = self._session.album(tidal_id)
            items: list[tidal.Track | tidal.Video] = []

            for i in range(math.ceil(tidal_obj.num_tracks + tidal_obj.num_videos / 100)):
                items.extend(tidal_obj.items(100, 100 * i))
            return [self._to_search_result(x) for x in items]
        if tidal_type == 'playlist':
            tidal_obj = self._session.playlist(tidal_id)
            items: list[tidal.Track | tidal.Video] = []

            for i in range(math.ceil(tidal_obj.num_tracks + tidal_obj.num_videos / 100)):
                items.extend(tidal_obj.items(100, 100 * i))
            return [self._to_search_result(x) for x in items if x.available]

        if tidal_type in ['track', 'video']:
            raise ValueError(f'TIDAL type {tidal_type} is not explorable!')
        raise ValueError(f'TIDAL type {tidal_type} is not a valid type!')

    def _check_mrid(self, mrid: str) -> tuple[str, str, MediaTypes, str]:
        """Split the MRID and check, if it has the right type."""
        provider_id, instance_id, tidal_type, tidal_id = mrid.split(':', 3)

        if provider_id != 'tidal':
            raise ValueError(
                f'The MRID ({mrid}) is not valid for this media provider (tidal),'
                'because the provider id\'s are not the same!'
            )

        if instance_id != self._instance_id:
            raise ValueError(
                f'The MRID ({mrid}) is not valid for this instance (tidal:{self._instance_id}),'
                'because the instance id\'s are not the same!'
            )

        return provider_id, instance_id, tidal_type, tidal_id

    def _get_track_or_video(self, mrid: str) -> tidal.Track | tidal.Video:
        """Get the track or video object for the given MRID."""
        _, _, tidal_type, tidal_id = self._check_mrid(mrid)

        if tidal_type == 'track':
            return self._session.track(tidal_id)
        if tidal_type == 'video':
            return self._session.video(tidal_id)

        if tidal_type in ['album', 'artist', 'playlist']:
            raise ValueError(f'TIDAL type {tidal_type} is not playable and has no metadata!')
        raise ValueError(f'TIDAL type {tidal_type} is not a valid type!')

    def resolve_mrid(self, mrid: str):
        """Get all the information of the given media resource like URI and metadata."""
        tidal_obj = self._get_track_or_video(mrid)

        if not tidal_obj.available:
            raise MediaNotAvailableException

        return MediaResource(
            provider=self,
            mrid=mrid,
            metadata=self.get_metadata(mrid),
            uri=tidal_obj.get_url(),
            continuous=False
        )

    def get_metadata(self, mrid: str):
        """Get the metadata of the given media resource."""
        tidal_obj = self._get_track_or_video(mrid)

        return Metadata(
            title=tidal_obj.name,
            artist=tidal_obj.artist.name,
            album=tidal_obj.album.name,
            image=self._get_image(tidal_obj),
            duration=tidal_obj.duration / 60
        )
