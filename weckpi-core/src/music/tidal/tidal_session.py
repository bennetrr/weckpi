"""Tools for interacting with a TIDAL session"""
import logging
from pathlib import Path

import tidalapi
import yaml

from music.metadata.now_playing import NowPlaying
from music.metadata.playlist_item import PlaylistItem
from music.tidal.search_result import SearchResult

logger = logging.getLogger(f'weckpi.{__name__}')

TidalModels = tidalapi.Artist | tidalapi.Album | tidalapi.Track | tidalapi.Video | tidalapi.Playlist


class TidalSession:
    """Represents a session with the TIDAL API"""
    session: tidalapi.Session

    def login(self, credential_file: Path) -> 'TidalSession':
        """
        Login to TIDAL using OAuth2.

        This method first tries to log in with the tokens stored in the credential file.
        If that fails, you will be asked to open a URL in your browser and log in with your TIDAL account.

        :param credential_file: The path to the credential file
        :return: The TIDAL session linked to your account
        :raises PermissionError: If the login failed
        """
        # Create a new tidal session
        self.session = tidalapi.Session()

        # Check if the credential file exists
        if credential_file.is_file():
            # Try to log in with the token in the credential file
            # TODO: Save the new token if the token needs to be refreshed
            with credential_file.open('r') as f:
                tidal_credential = yaml.load(f, yaml.SafeLoader)
            self.session.load_oauth_session(tidal_credential['token_type'],
                                            tidal_credential['access_token'],
                                            tidal_credential['refresh_token'])

            # Check if the session is valid
            if self.session.check_login():
                logger.info('Successfully logged in to Tidal')
                return self
            logger.warning('Could not log in to Tidal using the credential file')

        # Try to log in with simple OAuth2 login
        # TODO: Replace this with the login_oauth() method
        self.session.login_oauth_simple()

        if not self.session.check_login():
            raise PermissionError('Could not log in to Tidal')

        # Save the credential to the credential file
        with credential_file.open('w') as f:
            yaml.dump({
                'session_id': self.session.session_id,
                'access_token': self.session.access_token,
                'token_type': self.session.token_type,
                'refresh_token': self.session.refresh_token,
            }, f)

        logger.info('Successfully logged in to Tidal')
        return self

    def is_logged_in(self):
        """
        Check if the current session is valid

        :return: If the session is valid
        """
        return self.session.check_login()

    def search(self, query: str, artists: bool = True, albums: bool = True,
               tracks: bool = True, videos: bool = True, playlists: bool = True) -> SearchResult:
        """
        Search Tidal for the following term

        :param query: The term to search for
        :param artists: Search for artists
        :param albums: Search for albums
        :param tracks: Search for tracks
        :param videos: Search for music videos
        :param playlists: Search for playlists
        :return: The search result
        """
        models = []
        if artists:
            models.append(tidalapi.Artist)
        if albums:
            models.append(tidalapi.Album)
        if tracks:
            models.append(tidalapi.Track)
        if videos:
            models.append(tidalapi.Video)
        if playlists:
            models.append(tidalapi.Playlist)
        raw_results = self.session.search(query, models, limit=300)
        results = SearchResult.from_api_result(raw_results)
        return results

    def get_user_playlists(self) -> list[tidalapi.Playlist]:
        """Get the users playlists"""
        my_user = tidalapi.user.LoggedInUser(self.session, self.session.user.id)
        return my_user.playlists()

    # Saving and playback
    # noinspection PyMethodMayBeStatic
    def get_uri(self, obj: TidalModels) -> str:  # pylint: disable=R6301
        """
        Get the URI in the format ``tidal:<type>:<id>`` for the given object

        :raises TypeError: If the object is not a model of the TIDAL API
        """
        if isinstance(obj, tidalapi.Artist):
            uid = f'tidal:artist:{obj.id}'
        elif isinstance(obj, tidalapi.Album):
            uid = f'tidal:album:{obj.id}'
        elif isinstance(obj, tidalapi.Track):
            uid = f'tidal:track:{obj.id}'
        elif isinstance(obj, tidalapi.Video):
            uid = f'tidal:video:{obj.id}'
        elif isinstance(obj, tidalapi.Playlist):
            uid = f'tidal:playlist:{obj.id}'
        else:
            raise TypeError(f'The given object ({str(type(obj))}) is not a TIDAL API model')
        return uid

    # noinspection PyMethodMayBeStatic
    def get_mrl(self, obj: tidalapi.Track | tidalapi.Video) -> str:  # pylint: disable=R6301
        """
        Get the MRL for the given track or video

        :raises TypeError: If the object is not a TIDAL API track or a video
        :raises FileNotFoundError: If the track or video is not available on TIDAL
        """
        if not isinstance(obj, (tidalapi.Track, tidalapi.Video)):
            raise TypeError(f'The given object ({str(type(obj))}) is not a TIDAL API track or video')

        # Check if the track / video is available on TIDAL
        if not obj.available:
            raise FileNotFoundError(
                f'The track {obj.name} by {obj.artist.name} from {obj.album.name} is not available')

        mrl = obj.get_url()
        return mrl

    def get_mrls(self, obj: TidalModels | list[TidalModels]) -> list[str]:
        """
        Get the MRLs for the given object

        :raises TypeError: If the object is not a TIDAL API model or a list of TIDAL API models
        """
        # TODO: Check for availability
        # TODO: add offsetting
        if isinstance(obj, tidalapi.Artist):
            out = [self.get_mrl(item) for item in obj.get_top_tracks()]
        elif isinstance(obj, (tidalapi.Album, tidalapi.Playlist)):
            out = [self.get_mrl(item) for item in obj.tracks()]
        elif isinstance(obj, (tidalapi.Track, tidalapi.Video)):
            out = [self.get_mrl(obj)]
        elif isinstance(obj, list):
            out = []
            for item in obj:
                out.extend(self.get_mrls(item))
        else:
            raise TypeError(
                f'The given object ({str(type(obj))}) is not a TIDAL API model or a list of TIDAL API models')
        return out

    def resolve_uri(self, uri: str) -> TidalModels:
        """
        Get the TIDAL API object for the given URI

        :raises ValueError: If the URI is not in the correct format
        """
        uri_parts = uri.split(':', 2)

        if len(uri_parts) != 3:
            raise ValueError(f'The given URI ({uri}) is not in the correct format')

        prefix, model_type, uid = uri_parts

        if prefix != 'tidal':
            raise ValueError(f'The given URI ({uri}) is not in the correct format (does not begin with \'tidal:\')')

        if model_type == 'artist':
            obj = self.session.artist(uid)
        elif model_type == 'album':
            obj = self.session.album(uid)
        elif model_type == 'track':
            obj = self.session.track(uid)
        elif model_type == 'video':
            obj = self.session.video(uid)
        elif model_type == 'playlist':
            obj = self.session.playlist(uid)
        else:
            raise ValueError(f'Unknown model type {model_type})')
        return obj

    # noinspection PyMethodMayBeStatic
    def track_to_pli(self, track: tidalapi.Track | tidalapi.Video) -> PlaylistItem:  # pylint: disable=R6301
        """
        Get the playlist item object for the given track

        :raises TypeError: If the given object is not a TIDAL API track or video
        :raises FileNotFoundError: If the track is not available on TIDAL
        """
        if not isinstance(track, tidalapi.Track):
            raise TypeError(f'The given object ({str(type(track))}) is not a TIDAL API track')

        mrl = self.get_uri(track)
        title = track.name
        artist = track.artist.name
        album = track.album.name
        try:
            cover = track.album.image(1280)
        except AttributeError:
            cover = None

        return PlaylistItem(
            mrl,
            NowPlaying(title, artist, album, cover)
        )

    # noinspection PyMethodMayBeStatic
    def get_playlist_item(self, obj: TidalModels | list[TidalModels]) -> list[PlaylistItem]:  # pylint: disable=R6301
        """
        Get the playlist items object (NowPlaying-data + URI) for the given object

        :raises TypeError: If the object is not a TIDAL API model or a list of TIDAL API models
        :raises FileNotFoundError: If the object is an unavailable track or video
        """
        # TODO: add offsetting
        plis = []

        if isinstance(obj, tidalapi.Track | tidalapi.Video):
            plis.append(self.track_to_pli(obj))

        elif isinstance(obj, tidalapi.Artist):
            for track in obj.get_top_tracks():
                try:
                    plis.append(self.track_to_pli(track))
                except FileNotFoundError:
                    logger.warning(
                        f'Skipped non-available track {track.name} by {track.artist.name} from {track.album.name}')

        elif isinstance(obj, (tidalapi.Album, tidalapi.Playlist)):
            for track in obj.tracks():
                try:
                    plis.append(self.track_to_pli(track))
                except FileNotFoundError:
                    logger.warning(
                        f'Skipped non-available track {track.name} by {track.artist.name} from {track.album.name}')

        elif isinstance(obj, list):
            for item in obj:
                plis.extend(self.get_playlist_item(item))

        else:
            raise TypeError(
                f'The given object ({str(type(obj))}) is not a TIDAL API model or a list of TIDAL API models')

        return plis
