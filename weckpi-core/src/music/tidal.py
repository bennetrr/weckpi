"""Tools for interacting with Tidal"""
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Union

import tidalapi
import yaml

logger = logging.getLogger('weckpi.music.tidal')


@dataclass(repr=False, eq=False, order=False, frozen=True, kw_only=True)
class SearchResult:
    """Represents the search result from Tidal"""
    top_hit: Union[tidalapi.Artist, tidalapi.Album, tidalapi.Track, tidalapi.Video, tidalapi.Playlist]
    artists: list[tidalapi.Artist]
    albums: list[tidalapi.Album]
    tracks: list[tidalapi.Track]
    videos: list[tidalapi.Video]
    playlists: list[tidalapi.Playlist]

    @staticmethod
    def from_api_result(api_result: dict) -> 'SearchResult':
        return SearchResult(
            top_hit=api_result.get('top_hit', None),
            artists=api_result.get('artists', None),
            albums=api_result.get('albums', None),
            tracks=api_result.get('tracks', None),
            videos=api_result.get('videos', None),
            playlists=api_result.get('playlists', None)
        )


class TidalSession:
    """Represents a session with the Tidal api"""
    session: tidalapi.Session

    def login(self, credential_file: Path) -> 'TidalSession':
        """
        Log in to Tidal using OAuth2.
        If the credential file contains a valid access token, this is used to log in.
        Otherwise, you will be asked to open a browser and log in.
    
        :param credential_file: The path to the credential file
        :return: The Tidal session that you performed the login on
        """
        # Create a new tidal session
        self.session = tidalapi.Session()

        # Check if the credential file exists
        if credential_file.is_file():
            # Try to log in with the token in the credential file
            with credential_file.open('r') as f:
                tidal_credential = yaml.load(f, yaml.SafeLoader)
            self.session.load_oauth_session(tidal_credential['session_id'],
                                            tidal_credential['token_type'],
                                            tidal_credential['access_token'],
                                            tidal_credential['refresh_token'])

            # Check if the session is valid
            if self.session.check_login():
                logger.info('Successfully logged in to Tidal')
                return self
            logger.warning('Could not log in to Tidal using the credential file')

        # Try to log in with simple OAuth2 login
        # TODO Replace this with the login_oauth() method
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
        :return: The state of the session
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
        :return:
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
