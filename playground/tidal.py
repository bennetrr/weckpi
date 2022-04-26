import tidalapi
import yaml
import os
from rich.table import Table
from rich import print as rich_print

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

# Print out the users playlists
my_user = tidalapi.user.LoggedInUser(session, session.user.id)

my_playlists: list[tidalapi.playlist.Playlist] = my_user.playlists()

pl_table = Table(title='Playlists')
pl_table.add_column('Playlist Name', justify='left', style='cyan', overflow='crop', )
pl_table.add_column('Playlist UUID', justify='center', style='red', overflow='crop')
pl_table.add_column('Playlist Item Count', justify='right', style='green', overflow='crop')

for playlist in my_playlists:
    pl_table.add_row(playlist.name, str(playlist.id), str(playlist.num_tracks))

rich_print(pl_table)

# Get a specific playlist
playlist_name = input('Enter the playlist Name: ')

try:
    searched_playlist = list(filter(lambda pl: pl.name in playlist_name, my_playlists))[0]
except IndexError:
    print('Playlist not found!')
else:
    print(f'Found Playlist: {searched_playlist.name} ({searched_playlist.id}) with {searched_playlist.num_tracks} tracks')
    print('Contains:')
    for uuid, track in enumerate(searched_playlist.tracks()):
        print(f'{uuid + 1}. {track.artist.name} - {track.name} ({track.id})')
