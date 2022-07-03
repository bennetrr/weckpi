"""
End-to-end test initializer for TIDAL

Run this script with the IntelliJ Python Console to interact with the player
"""
import logging
from pathlib import Path

from music.players.playlist_player import PlaylistPlayer
from music.tidal.tidal_session import TidalSession
from utils.logging import format_logger

logger = logging.getLogger('weckpi.e2e.tidal')

if __name__ == '__main__':
    format_logger(logger)

    logger.info('Test initialisation started')

    # Log in to TIDAL
    session = TidalSession().login(Path('tidal.credential.yaml'))
    logger.debug('Login successful')

    # Search for VNV Nation and select the first album
    search_results = session.search('VNV Nation')
    album = search_results.albums[0]
    logger.debug(f'Searched for VNV Nation, first album: {album.name} with {len(album.tracks())} tracks')

    # Convert the album in our format
    playlist = session.get_playlist_item(album)

    # Create a new player and play the album
    player = PlaylistPlayer(playlist, tidal_session=session)
    player.play()

    logger.info('Test initialisation finished')
    logger.info('You can now start to test the player')
