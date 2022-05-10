import logging
from pathlib import Path

import yaml
from tidalapi import Session

logger = logging.getLogger('weckpi.music.tidal')


def login(credentials_file: Path) -> Session:
    """
    Login to Tidal using OAuth2. If the credentials file contains a valid access token, this is used to log in. Otherwise you will asked to open a browser and login.

    :param credentials_file: The path to the credentials file
    :return: The Tidal session
    """
    # TODO Write tests
    # Create a new tidal session
    session = Session()

    # Check if the credentials file exists
    if credentials_file.is_file():
        # Try to log in with the token in the credentials file
        with credentials_file.open('r') as f:
            tidal_credentials = yaml.load(f, yaml.SafeLoader)
        session.load_oauth_session(tidal_credentials['session_id'],
                                   tidal_credentials['token_type'],
                                   tidal_credentials['access_token'],
                                   tidal_credentials['refresh_token'])

        # Check if the session is valid
        if session.check_login():
            logger.info('Successfully logged in to Tidal')
            return session
        logger.warning('Could not log in to Tidal using the credentials file')

    # Try to log in with simple OAuth2 login
    # TODO Replace this with the login_oauth() method
    session.login_oauth_simple()

    if not session.check_login():
        raise PermissionError('Could not log in to Tidal')

    # Save the credentials to the credentials file
    with credentials_file.open('w') as f:
        yaml.dump({
            'session_id': session.session_id,
            'access_token': session.access_token,
            'token_type': session.token_type,
            'refresh_token': session.refresh_token,
        }, f)

    logger.info('Successfully logged in to Tidal')
    return session
