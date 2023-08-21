"""All music related configuration models."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from weckpi.api.authentication import OAuthSession


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
            } if self.auth_session else None
        }
