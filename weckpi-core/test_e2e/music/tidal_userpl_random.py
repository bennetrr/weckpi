"""
End-to-end test initializer for TIDAL

Run this script with the IntelliJ Python Console to interact with the player
"""
import logging
import time
from pathlib import Path

import keyboard
import tidalapi

from music.players.random_playlist_player import RandomPlaylistPlayer
from music.tidal.tidal_session import TidalSession
from utils.logging import format_logger

logger = logging.getLogger('weckpi.e2e.tidal')

if __name__ == '__main__':
    format_logger(logger)

    logger.info('Test initialisation started')

    # Log in to TIDAL
    session = TidalSession().login(Path('tidal.credential.yaml'))
    logger.debug('Login successful')

    # Get the user's playlists and select the one with the name "Synthpop"
    user_playlists = session.get_user_playlists()

    synthpop_playlist: tidalapi.Playlist | None = None
    for user_playlist in user_playlists:
        if user_playlist.name == 'Synthpop':
            synthpop_playlist = user_playlist

    if synthpop_playlist is None:
        raise FileNotFoundError('Synthpop playlist not found')

    logger.debug(f'Found Synthpop playlist with {len(synthpop_playlist.tracks())} tracks')

    # Convert the playlist in our format
    playlist = session.get_playlist_item(synthpop_playlist)

    # Create a new player and play the album
    player = RandomPlaylistPlayer(playlist, tidal_session=session)
    player.play()

    logger.info('Test initialisation finished')
    logger.info('You can now start to test the player')

    print('''Key usage:
    q: quit
    p: play / pause
    s: stop
    n: next track
    b: previous track
    j: jump to a given track
    i: show which track is currently playing
    +: increase volume by 5%
    -: decrease volume by 5%
    ''')

    while True:
        if keyboard.is_pressed('q'):
            logger.info('Quitting')
            player.stop()
            break

        if keyboard.is_pressed('p'):
            if player.is_playing:
                logger.info('Pausing')
                player.pause()
            else:
                logger.info('Playing')
                player.play()

        if keyboard.is_pressed('s'):
            logger.info('Stopping')
            player.stop()

        if keyboard.is_pressed('n'):
            logger.info('Next track')
            player.next()

        if keyboard.is_pressed('b'):
            logger.info('Previous track')
            player.previous()

        if keyboard.is_pressed('j'):
            index = int(input('Enter index: '))
            logger.info(f'Jumping to track {index}')
            player.jump_to(index)

        if keyboard.is_pressed('i'):
            if player.is_playing:
                print(f'{player.now_playing} ({player.playlist_index} / {player.playlist_length}) {player.position}% played')
            else:
                print(f'Player is not playing')

        if keyboard.is_pressed('+'):
            player.volume += 5
            time.sleep(0.1)
            logger.info(f'Volume increased to {player.volume}')

        if keyboard.is_pressed('-'):
            player.volume -= 5
            time.sleep(0.1)
            logger.info(f'Volume decreased to {player.volume}')

        player.event_loop()
        time.sleep(0.1)
