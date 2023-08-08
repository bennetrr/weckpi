"""The data structure for the configuration."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from weckpi.api.authentication import OAuthSession


@dataclass
class WeckPiConfig:
    """
    The root config model.

    :var music: Config for the music system.
    """
    music: MusicConfig

    @classmethod
    def from_json(cls, config_file: Path) -> WeckPiConfig:
        """Create a WeckPiConfig object from a json file."""
        with config_file.open('r', encoding='utf-8') as config_stream:
            config_json: dict = json.load(config_stream)

        return cls(
            MusicConfig.from_json(config_json['music'])
        )

    def to_json(self, config_file: Path) -> None:
        """Save this WeckPiConfig object to a json file."""
        config_json = {
            'music': self.music.to_json()
        }

        with config_file.open('w', encoding='utf-8') as config_stream:
            json.dump(config_json, config_stream, indent=4)


@dataclass
class MusicConfig:
    """
    The root model for the music system config.

    :var active_media_player: The UID of the media player that is currently used to play music.
    :var media_provider_instances: A list of instances for each registered media provider.
        This is only used for creating the instances and loading previous authentication sessions,
        if you need to work with an instance,
        use the :py:class:`~weckpi.api.plugin_manager.plugin_manager.PluginManager`.
    """
    active_media_player: str
    media_provider_instances: dict[str, list[MediaProviderInstanceConfig]]

    @classmethod
    def from_json(cls, config_json: dict) -> MusicConfig:
        """Create a MusicConfig object from a dict."""
        return cls(
            config_json['activeMediaPlayer'],
            {
                key: [
                    MediaProviderInstanceConfig.from_json(item) for item in val
                ] for key, val in config_json['mediaProviderInstances'].items()
            }
        )

    def to_json(self) -> dict:
        """Dump this MusicConfig object into a dict."""
        return {
            'activeMediaPlayer': self.active_media_player,
            'mediaProviderInstances': {
                key: [
                    item.to_json() for item in val
                ] for key, val in self.media_provider_instances.items()
            }
        }


@dataclass
class MediaProviderInstanceConfig:
    """
    Configuration for an instance of a media provider.

    This is only used for creating the instances and loading previous authentication sessions,
    if you need to work with an instance, use the :py:class:`~weckpi.api.plugin_manager.plugin_manager.PluginManager`.

    :var uid: The UID of this provider instance.
    :var auth_session: A saved authentication session, if the user has already logged in to this provider.
    """
    uid: str
    auth_session: OAuthSession | None = None

    @classmethod
    def from_json(cls, config_json: dict):
        """Create a MediaProviderInstanceConfig object from a dict."""
        return cls(
            config_json['uid'],
            OAuthSession(
                config_json['authSession']['tokenType'],
                config_json['authSession']['accessToken'],
                config_json['authSession']['refreshToken'],
                datetime.fromisoformat(config_json['authSession']['expireTime'])
            ) if config_json.get('authSession') else None
        )

    def to_json(self) -> dict:
        """Dump this MediaProviderInstanceConfig object into a dict."""
        return {
            'uid': self.uid,
            'authSession': {
                'tokenType': self.auth_session.token_type,
                'accessToken': self.auth_session.access_token,
                'refreshToken': self.auth_session.refresh_token,
                'expireTime': self.auth_session.expire_time.isoformat()
            }
        }


_config_instance: WeckPiConfig | None = None


def config(config_file: Path = None) -> WeckPiConfig:
    """Get the configuration object."""
    global _config_instance
    if _config_instance is None:
        _config_instance = WeckPiConfig.from_json(config_file)
    return _config_instance
