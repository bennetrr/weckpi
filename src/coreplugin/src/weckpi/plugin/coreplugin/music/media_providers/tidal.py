"""Media provider for the streaming service TIDAL that uses the package `tidalapi <https://tidalapi.netlify.app/>`_."""
from __future__ import annotations

import logging
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Literal

import tidalapi as tidal

from weckpi.api.authentication import AuthenticationResult, CodeAuthenticationDetails, LinkAuthenticationDetails, \
    OAuthSession
from weckpi.api.music import MediaNotAvailableException, MediaProvider, MediaResource, Metadata, SearchResult

logger = logging.getLogger(__name__)

MediaTypes = Literal['album', 'artist', 'track', 'video', 'playlist']


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

    def search(self, search_term: str):
        """Search TIDAL for the search term."""
        # TODO Reduce duplication
        res = self._session.search(search_term)

        return [
            *[SearchResult(
                mrid=f'tidal:{self._instance_id}:album:{x.id}',
                is_media_resource=False,
                name=x.name,
                text=f'Album von {x.artist.name}',  # TODO Localization
                image=x.image(1280)
            ) for x in res['albums']],

            *[SearchResult(
                mrid=f'tidal:{self._instance_id}:artist:{x.id}',
                is_media_resource=False,
                name=x.name,
                image=x.image(750)
            ) for x in res['artists']],

            *[SearchResult(
                mrid=f'tidal:{self._instance_id}:track:{x.id}',
                is_media_resource=True,
                name=x.name,
                text=f'Song von {x.artist.name}',  # TODO Localization
                image=x.album.image(1280)
            ) for x in res['tracks']],

            *[SearchResult(
                mrid=f'tidal:{self._instance_id}:video:{x.id}',
                is_media_resource=True,
                name=x.name,
                text=f'Video von {x.artist.name}',  # TODO Localization
                image=x.album.image(1280)
            ) for x in res['videos']],

            *[SearchResult(
                mrid=f'tidal:{self._instance_id}:playlist:{x.id}',
                is_media_resource=False,
                name=x.name,
                text=f'Playlist{("von " + x.creator.name) if x.creator else ""}',  # TODO Localization
                image=x.image(1080)
            ) for x in res['playlists']]]

    def explore(self, mrid: str = None):
        """
        List the content that is available under the given MRID.

        :param mrid: Must be the MRID of type ``artist``, ``album`` or ``playlist``.
                     If omitted or ``None``, the "My ..." elements are returned.
        """
        # TODO Reduce duplication
        if mrid is None:
            mrid = f'tidal:{self._instance_id}:library:overview'

        _, _, tidal_type, tidal_id = self._check_mrid(mrid)

        if tidal_type == 'library':
            if tidal_id == 'overview':
                return [
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:library:playlists',
                        is_media_resource=False,
                        name=f'Playlists',  # TODO Localization
                        image=''  # TODO Image
                    ),
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:library:artists',
                        is_media_resource=False,
                        name=f'Künstler',  # TODO Localization
                        image=''  # TODO Image
                    ),
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:library:albums',
                        is_media_resource=False,
                        name=f'Alben',  # TODO Localization
                        image=''  # TODO Image
                    ),
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:library:tracks',
                        is_media_resource=False,
                        name=f'Songs',  # TODO Localization
                        image=''  # TODO Image
                    ),
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:library:videos',
                        is_media_resource=False,
                        name=f'Videos',  # TODO Localization
                        image=''  # TODO Image
                    ),
                ]
            if tidal_id == 'playlists':
                playlists: list[tidal.Playlist] = [
                    *self._session.user.playlists(),
                    *self._session.user.favorites.playlists()
                ]

                return [
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:playlist:{x.id}',
                        is_media_resource=False,
                        name=x.name,
                        text=f'Playlist von {x.creator.name}',  # TODO Localization
                        image=x.image(1080)
                    ) for x in playlists
                ]
            if tidal_id == 'artists':
                artists: list[tidal.Artist] = self._session.user.favorites.artists()

                return [
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:artist:{x.id}',
                        is_media_resource=False,
                        name=x.name,
                        image=''  # x.image(750)
                    ) for x in artists
                ]
            if tidal_id == 'albums':
                albums: list[tidal.Album] = self._session.user.favorites.albums()

                return [
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:album:{x.id}',
                        is_media_resource=False,
                        name=x.name,
                        text=f'Album von {x.artist.name}',  # TODO Localization
                        image=x.image(1280)
                    ) for x in albums
                ]
            if tidal_id == 'tracks':
                tracks: list[tidal.Track] = self._session.user.favorites.tracks()

                return [
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:track:{x.id}',
                        is_media_resource=True,
                        name=x.name,
                        text=f'Song von {x.artist.name}',  # TODO Localization
                        image=x.album.image(1280)
                    ) for x in tracks
                ]
            if tidal_id == 'videos':
                videos: list[tidal.Video] = self._session.user.favorites.videos()

                return [
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:video:{x.id}',
                        is_media_resource=True,
                        name=x.name,
                        text=f'Song von {x.artist.name}',  # TODO Localization
                        image=x.album.image(1280)
                    ) for x in videos
                ]
            raise ValueError(f'TIDAL type library:{tidal_id} is not a valid type!')
        if tidal_type == 'playlist':
            items: list[tidal.Track | tidal.Video] = self._session.playlist(tidal_id).items()  # TODO Use offset
            items.extend(self._session.playlist(tidal_id).items(100, 100))

            result: list[SearchResult] = []

            for x in items:
                if not x.available:
                    continue

                if isinstance(x, tidal.Track):
                    result.append(
                        SearchResult(
                            mrid=f'tidal:{self._instance_id}:track:{x.id}',
                            is_media_resource=True,
                            name=x.name,
                            text=f'Song von {x.artist.name}',  # TODO Localization
                            image=x.album.image(1280)
                        )
                    )
                elif isinstance(x, tidal.Video):
                    result.append(
                        SearchResult(
                            mrid=f'tidal:{self._instance_id}:video:{x.id}',
                            is_media_resource=True,
                            name=x.name,
                            text=f'Video von {x.artist.name}',  # TODO Localization
                            image=x.album.image(1280)
                        )
                    )

            return result
        if tidal_type == 'artist':
            if tidal_id.endswith(':allTracks'):
                return [
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:track:{x.id}',
                        is_media_resource=True,
                        name=x.name,
                        text=f'Song von {x.artist.name}',
                        image=x.album.image(1280)
                    ) for x in self._session.artist(tidal_id.removesuffix(':allTracks')).get_top_tracks()
                ]

            albums: list[tidal.Album] = [
                *self._session.artist(tidal_id).get_albums(),
                *self._session.artist(tidal_id).get_albums_ep_singles(),
                *self._session.artist(tidal_id).get_albums_other()
            ]

            result: list[SearchResult] = [
                SearchResult(
                    mrid=f'{mrid}:allTracks',
                    is_media_resource=False,
                    name='Alle Songs',
                    image=''  # TODO Image
                )
            ]

            for x in albums:
                result.append(
                    SearchResult(
                        mrid=f'tidal:{self._instance_id}:album:{x.id}',
                        is_media_resource=False,
                        name=x.name,
                        text=f'Album von {x.artist.name}',  # TODO Localization
                        image=x.image(1280)
                    )
                )
            return result
        if tidal_type == 'album':
            items: list[tidal.Track | tidal.Video] = self._session.album(tidal_id).items()  # TODO Use offset

            result: list[SearchResult] = []

            for x in items:
                if isinstance(x, tidal.Track):
                    result.append(
                        SearchResult(
                            mrid=f'tidal:{self._instance_id}:track:{x.id}',
                            is_media_resource=True,
                            name=x.name,
                            text=f'Song von {x.artist.name}',  # TODO Localization
                            image=x.album.image(1280)
                        )
                    )
                elif isinstance(x, tidal.Video):
                    result.append(
                        SearchResult(
                            mrid=f'tidal:{self._instance_id}:video:{x.id}',
                            is_media_resource=True,
                            name=x.name,
                            text=f'Video von {x.artist.name}',  # TODO Localization
                            image=x.album.image(1280)
                        )
                    )

            return result

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

    def resolve_mrid(self, mrid: str):
        """Get all the information of the given media resource like URI and metadata."""
        # TODO Reduce duplication
        _, _, tidal_type, tidal_id = self._check_mrid(mrid)

        if tidal_type == 'track':
            tidal_obj = self._session.track(tidal_id)

            if not tidal_obj.available:
                raise MediaNotAvailableException

            return MediaResource(
                provider=self, mrid=mrid, metadata=self.get_metadata(mrid), uri=tidal_obj.get_url(), continuous=False
            )

        if tidal_type == 'video':
            tidal_obj = self._session.video(tidal_id)

            if not tidal_obj.available:
                raise MediaNotAvailableException

            return MediaResource(
                provider=self, mrid=mrid, metadata=self.get_metadata(mrid), uri=tidal_obj.get_url(), continuous=False
            )

        if tidal_type in ['album', 'artist', 'playlist']:
            raise ValueError(f'TIDAL type {tidal_type} is not playable and cannot be resolved!')

        raise ValueError(f'TIDAL type {tidal_type} is not a valid type!')

    def get_metadata(self, mrid: str):
        """Get the metadata of the given media resource."""
        # TODO Reduce duplication
        _, _, tidal_type, tidal_id = self._check_mrid(mrid)

        if tidal_type == 'track':
            tidal_obj = self._session.track(tidal_id)

            return Metadata(
                title=tidal_obj.name,
                artist=tidal_obj.artist.name,
                album=tidal_obj.album.name,
                image=tidal_obj.album.image(1280),
                duration=tidal_obj.duration / 60
            )

        if tidal_type == 'video':
            tidal_obj = self._session.video(tidal_id)

            return Metadata(
                title=tidal_obj.name,
                artist=tidal_obj.artist.name,
                album=tidal_obj.album.name,
                image=tidal_obj.image(),
                duration=tidal_obj.duration / 60
            )

        if tidal_type in ['album', 'artist', 'playlist']:
            raise ValueError(f'TIDAL type {tidal_type} is not playable and has no metadata!')

        raise ValueError(f'TIDAL type {tidal_type} is not a valid type!')
