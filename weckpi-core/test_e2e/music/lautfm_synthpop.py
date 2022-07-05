"""
End-to-end test initializer for internet radio using Synthpop Radio @ Laut.FM

Run this script with the IntelliJ Python Console to interact with the player
"""
import logging

from music.metadata.internet_radio_metadata.lautfm_metadata import LautFmMetadataApi
from music.players.internet_radio import InternetRadioPlayer
from utils.logging import format_logger

logger = logging.getLogger('weckpi.e2e.internet_radio')

if __name__ == '__main__':
    format_logger(logger)

    logger.info('Test initialisation started')

    # Create the metadata API
    metadata_api = LautFmMetadataApi('synthpop')

    # Create a new player and start the radio
    player = InternetRadioPlayer('https://stream.laut.fm/synthpop', metadata_api)
    player.play()

    logger.info('Test initialisation finished')
    logger.info('You can now start to test the player')
