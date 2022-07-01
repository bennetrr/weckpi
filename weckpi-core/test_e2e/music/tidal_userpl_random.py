"""
End-to-end test initializer for TIDAL

Run this script with the IntelliJ Python Console to interact with the player
"""
import logging
from pathlib import Path

import tidalapi

from music.players.playlist_player import PlaylistPlayer as RandomPlaylistPlayer
from music.tidal.tidal_session import TidalSession
from utils.logging import format_logger

logger = logging.getLogger('weckpi.e2e.tidal')

if __name__ == '__main__':
    format_logger(logger)

    logger.info('Test initialisation started')

    # Log in to TIDAL
    session = TidalSession().login(Path('tidal.credential.yaml'))
    logger.debug('Login successful')

    # Get the users playlists and select the one with the name "Synthpop"
    user_playlists = session.get_user_playlists()

    synthpop_playlist: tidalapi.Playlist | None = None
    for user_playlist in user_playlists:
        if user_playlist.name == 'Synthpop':
            synthpop_playlist = user_playlist

    if synthpop_playlist is None:
        raise AssertionError('Synthpop playlist not found')

    logger.debug(f'Found Synthpop playlist with {len(synthpop_playlist.tracks())} tracks')

    # Convert the playlist in our format
    playlist = session.get_playable_data(synthpop_playlist)

    # Create a new player and play the album
    player = RandomPlaylistPlayer(playlist)
    player.play()

    logger.info('Test initialisation finished')
    logger.info('You can now start to test the player')
