import tidalapi
import yaml
import os

# Log in to TIDAL
session = tidalapi.Session()

# Check, if the file tidal_credentials.yaml exists
if os.path.isfile('tidal_credentials.yaml'):
    with open('tidal_credentials.yaml', 'r') as f:
        tidal_credentials = yaml.load(f, yaml.SafeLoader)
    session.load_oauth_session(tidal_credentials['session_id'],
                               tidal_credentials['token_type'],
                               tidal_credentials['access_token'],
                               tidal_credentials['refresh_token'])
else:
    session.login_oauth_simple()

    # Save the session for later use
    with open('tidal_credentials.yaml', 'w') as f:
        yaml.dump({
            'session_id':    session.session_id,
            'access_token':  session.access_token,
            'token_type':    session.token_type,
            'refresh_token': session.refresh_token,
        }, f)

# Check if the login was successful
if not session.check_login():
    print('Login failed!')
    exit(1)
print('Login successful!')
