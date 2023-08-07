"""Tests for the config package."""
from datetime import datetime
from pathlib import Path

from weckpi.api.authentication import OAuthSession
from weckpi.api.config.config_structure import MediaProviderInstanceConfig, MusicConfig, WeckPiConfig, config


def test_config_parser():
    """Test if the config is correctly parsed."""
    # Arrange
    manual_config = WeckPiConfig(
        music=MusicConfig(
            active_media_player='mpv',
            media_provider_instances={
                'localFs': [
                    MediaProviderInstanceConfig(
                        uid='localFs',
                        auth_session=None
                    )
                ],
                'tidal': [
                    MediaProviderInstanceConfig(
                        uid='demo',
                        auth_session=OAuthSession(
                            token_type='Bearer',
                            access_token='...',
                            refresh_token='...',
                            expire_time=datetime(2023, 8, 7, 22, 23, 37, 995140)
                        )
                    )
                ]
            }
        )
    )

    config_file = Path('sampleConfig.json')

    # Act
    parsed_config = config(config_file)

    # Assert
    assert parsed_config == manual_config


# TODO Add tests for changing and saving the config
