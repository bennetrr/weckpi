from __future__ import annotations

from json import JSONDecodeError
from pathlib import Path
import json
from concurrent.futures import Future, ThreadPoolExecutor

import tidalapi as tidal

from weckpi.api.music import MediaProvider, MediaResource, Metadata
from weckpi.api.authentication import LinkAuthenticationResponse, CodeAuthenticationResponse


class Tidal(MediaProvider):
    """"""
    _session: tidal.Session
    _session_id: str

    def __init__(self, session_id: str):
        session_config = tidal.Config()
        self._session = tidal.Session(session_config)
        self._session_id = session_id

    def login(self, credential_file: Path):
        """Log in with your Tidal Account."""
        if credential_file.is_file():
            print('Trying with credential file')
            with credential_file.open(mode='r', encoding='utf-8') as credential_stream:
                try:
                    credential_json = json.load(credential_stream)

                    session_restore_successful = self._session.load_oauth_session(
                        credential_json['token_type'],
                        credential_json['access_token'],
                        credential_json['refresh_token']
                    )
                except JSONDecodeError:
                    session_restore_successful = False

            if session_restore_successful:
                print('Session successfully restored from credential file')
                with credential_file.open('w', encoding='utf-8') as credential_stream:
                    json.dump({
                        'token_type': self._session.token_type,
                        'access_token': self._session.access_token,
                        'refresh_token': self._session.refresh_token
                    }, credential_stream, indent=2)
                return

        print('First login')
        login, future = self._session.login_oauth()
        print('Requested')
        executor = ThreadPoolExecutor()
        promise = executor.submit(self._login, credential_file, future)
        print('Executed')

        return (
            CodeAuthenticationResponse(promise, login.expires_in, login.verification_uri, login.user_code),
            LinkAuthenticationResponse(promise, login.expires_in, login.verification_uri_complete)
        )

    def _login(self, credential_file: Path, promise: Future):
        """Second step of login"""
        promise.result()
        print('Login successful')

        with credential_file.open('w', encoding='utf-8') as credential_stream:
            json.dump({
                'token_type': self._session.token_type,
                'access_token': self._session.access_token,
                'refresh_token': self._session.refresh_token
            }, credential_stream, indent=2)
        return

    def search(self, search_term: str) -> list[str]:
        res = self._session.search(search_term)
        return [
            *[f'tidal:{self._session_id}:album:{x.id}' for x in res['albums']],
            *[f'tidal:{self._session_id}:artist:{x.id}' for x in res['artists']],
            *[f'tidal:{self._session_id}:track:{x.id}' for x in res['tracks']],
            *[f'tidal:{self._session_id}:video:{x.id}' for x in res['videos']],
            *[f'tidal:{self._session_id}:playlist:{x.id}' for x in res['playlists']]
        ]

    def explore(self, path: str = ...) -> list[str]:
        if path is None:
            path = f'tidal:{self._session_id}:my_playlists'
        ...

    def resolve_mrid(self, mrid: str) -> MediaResource:
        _, _, tidal_type, tidal_id = mrid.split(':', 3)

        if tidal_type == 'track':
            tidal_obj = self._session.track(tidal_id)

            return MediaResource(
                provider=self,
                mrid=mrid,
                metadata=Metadata(
                    title=tidal_obj.name,
                    artist=tidal_obj.artist.name,
                    album=tidal_obj.album.name,
                    image=tidal_obj.album.image(1280),
                    played_from='TIDAL'
                ),
                uri=tidal_obj.get_url(),
                continuous=False
            )
        if tidal_type == 'video':
            raise NotImplementedError
        raise NotImplementedError

    def get_metadata(self, mrid: str) -> Metadata:
        pass
