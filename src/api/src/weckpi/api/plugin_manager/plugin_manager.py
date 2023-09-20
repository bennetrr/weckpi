"""The plugin manager singleton class."""
from __future__ import annotations

from typing import Type

import weckpi.api.music as wpm
from .registration_details import MediaPlayerRegistration, MediaProviderRegistration

# TODO Better plugin manager without duplicating the same code over and over
#  The new plugin manager should also create the instances itself and hand over parameters automatically


class PluginManager:
    """
    The plugin manager singleton class.

    This class is responsible for registering the plugins and allowing other plugins to communicate with each other.
    """
    _media_providers: dict[str, MediaProviderRegistration]
    _media_players: dict[str, MediaPlayerRegistration]

    def __init__(self):
        self._media_providers = {}
        self._media_players = {}

    def register_media_provider(self, name: str, cls: Type[wpm.MediaProvider], needs_login: bool, has_search: bool,
                                has_explore: bool) -> None:
        """Register a media provider to the plugin manager."""
        if name in self._media_providers:
            raise RuntimeError(f'The media provider {name} is already registered!')
        self._media_providers[name] = MediaProviderRegistration(name, cls, needs_login, has_search, has_explore)

    def get_media_provider(self, name: str) -> MediaProviderRegistration:
        """Get a registered media provider from the plugin manager."""
        if name not in self._media_providers:
            raise KeyError(f'The media provider {name} is not registered!')
        return self._media_providers[name]

    def register_media_player(self, name: str, cls: Type[wpm.MediaPlayer]):
        """Register a media player to the plugin manager."""
        if name in self._media_players:
            raise RuntimeError(f'The media player {name} is already registered!')
        self._media_players[name] = MediaPlayerRegistration(name, cls)

    def get_media_player(self, name: str) -> MediaPlayerRegistration:
        """Get a registered media player from the plugin manager."""
        if name not in self._media_players:
            raise KeyError(f'The media player {name} is not registered!')
        return self._media_players[name]


_plugin_manager_instance: PluginManager | None = None


def plugin_manager() -> PluginManager:
    """Get the plugin manager object."""
    global _plugin_manager_instance
    if _plugin_manager_instance is None:
        _plugin_manager_instance = PluginManager()
    return _plugin_manager_instance
