from __future__ import annotations

from typing import Type

import weckpi.api.music as wpm
from .registration_details import MediaProviderRegistration, MediaPlayerRegistration


class PluginManager:
    _instance: PluginManager = None

    _media_providers: dict[str, MediaProviderRegistration]
    _media_players: dict[str, MediaPlayerRegistration]

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = PluginManager()
        return cls._instance

    def __init__(self):
        self._media_providers = {}
        self._media_players = {}

    def register_media_provider(self, name: str, cls: Type[wpm.MediaProvider], needs_login: bool, has_search: bool,
                                has_explore: bool):
        if name in self._media_providers:
            raise RuntimeError(f'The media provider {name} is already registered!')
        self._media_providers[name] = MediaProviderRegistration(name, cls, needs_login, has_search, has_explore)

    def get_media_provider(self, name: str) -> MediaProviderRegistration:
        if name not in self._media_providers:
            raise KeyError(f'The media provider {name} is not registered!')
        return self._media_providers[name]

    def register_media_player(self, name: str, cls: Type[wpm.MediaPlayer]):
        if name in self._media_players:
            raise RuntimeError(f'The media player {name} is already registered!')
        self._media_players[name] = MediaPlayerRegistration(name, cls)

    def get_media_player(self, name: str) -> MediaPlayerRegistration:
        if name not in self._media_players:
            raise KeyError(f'The media player {name} is not registered!')
        return self._media_players[name]
