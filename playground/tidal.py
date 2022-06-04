"""Experimenting with the tidal api"""
# pylint: disable-all
from pathlib import Path

import tidalapi
from rich import print as rich_print
from rich.table import Table

from music.tidal.tidal_session import TidalSession

# Log in to TIDAL
session = TidalSession().login(Path('tidal_credential.yaml'))

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
    print(
        f'Found Playlist: {searched_playlist.name} ({searched_playlist.id}) with {searched_playlist.num_tracks} tracks')
    print('Contains:')
    for uuid, track in enumerate(searched_playlist.tracks()):
        print(f'{uuid + 1}. {track.artist.name} - {track.name} ({track.id})')
