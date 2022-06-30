"""Tools for interacting with a TIDAL session"""
import logging
from pathlib import Path

import tidalapi
import yaml

from music.metadata.now_playing import NowPlaying
from music.metadata.playlist_item import PlaylistItem
from music.tidal.search_result import SearchResult

logger = logging.getLogger(f'weckpi.{__name__}')


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

    @staticmethod
    def get_id(obj: tidalapi.Artist | tidalapi.Album | tidalapi.Track | tidalapi.Video | tidalapi.Playlist) -> str:
        """
        Get the ID in the format type+id for the given object

        :param obj: An object of the TIDAL API
        :return: The ID
        :raises ValueError: If the object is not of the TIDAL API
        """
        if isinstance(obj, tidalapi.Artist):
            uid = f'artist+{obj.id}'
        elif isinstance(obj, tidalapi.Album):
            uid = f'album+{obj.id}'
        elif isinstance(obj, tidalapi.Track):
            uid = f'track+{obj.id}'
        elif isinstance(obj, tidalapi.Video):
            uid = f'video+{obj.id}'
        elif isinstance(obj, tidalapi.Playlist):
            uid = f'playlist+{obj.id}'
        else:
            raise ValueError('Unknown object type')
        return uid

    def resolve_id(self, uid) \
            -> tidalapi.Artist | tidalapi.Album | tidalapi.Track | tidalapi.Video | tidalapi.Playlist:
        """
        Get the TIDAL object for the given ID in the format type+id

        :param uid: The ID
        :return: The TIDAL object
        :raises ValueError: If the ID is not in the correct format
        """
        model_type, new_uid = uid.split('+')

        if model_type == 'artist':
            obj = self.session.artist(new_uid)
        elif model_type == 'album':
            obj = self.session.album(new_uid)
        elif model_type == 'track':
            obj = self.session.track(new_uid)
        elif model_type == 'video':
            obj = self.session.video(new_uid)
        elif model_type == 'playlist':
            obj = self.session.playlist(new_uid)
        else:
            raise ValueError('Unknown object type')

        return obj

    @staticmethod
    def track_to_playlist_item(track: tidalapi.Track) -> PlaylistItem:
        """Convert a TIDAL API track into a PlaylistItem"""
        if not track.available:
            raise FileNotFoundError(
                f'The track {track.name} by {track.artist.name} from {track.album.name} is not available')
        mrl = track.get_url()
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

    @staticmethod
    def get_playable_data(
            obj: tidalapi.Artist | tidalapi.Album | tidalapi.Track | tidalapi.Video | tidalapi.Playlist |
                 list[tidalapi.Artist | tidalapi.Album | tidalapi.Track | tidalapi.Video | tidalapi.Playlist]) -> \
            list[PlaylistItem]:
        """Get the mrl and the now playing metadata of the TIDAL API object"""
        if isinstance(obj, tidalapi.Video):
            raise TypeError('Music videos are not (yet) supported')

        track_to_pli = TidalSession.track_to_playlist_item

        if isinstance(obj, tidalapi.Track):
            return [track_to_pli(obj)]

        if isinstance(obj, (tidalapi.Playlist, tidalapi.Album)):
            output_list: list[PlaylistItem] = []

            for track in obj.tracks():  # TODO: add offsetting
                try:
                    output_list.append(track_to_pli(track))
                except FileNotFoundError:
                    logger.warning(
                        f'Skipped non-available track {track.name} by {track.artist.name} from {track.album.name}')

            return output_list

        if isinstance(obj, tidalapi.Artist):
            output_list: list[PlaylistItem] = []

            for track in obj.get_top_tracks():  # TODO: add offsetting
                try:
                    output_list.append(track_to_pli(track))
                except FileNotFoundError:
                    logger.warning(
                        f'Skipped non-available track {track.name} by {track.artist.name} from {track.album.name}')

            return output_list

        if isinstance(obj, list):
            output_list: list[PlaylistItem] = []

            for item in obj:
                output_list.extend(TidalSession.get_playable_data(item))

            return output_list

        raise TypeError(f'Unsupported TIDAL API model: {type(obj)}')
