"""The data structure for the configuration."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from weckpi.api.authentication import OAuthCredentials


@dataclass
class WeckPiConfig:
    music: MusicConfig

    def __init__(self, config_file: Path):
        ...


@dataclass
class MusicConfig:
    media_providers: list[MediaProviderConfig]
    active_media_player: str


@dataclass
class MediaProviderConfig:
    name: str
    instances: list[MediaProviderInstanceConfig]


@dataclass
class MediaProviderInstanceConfig:
    name: str
    credentials: OAuthCredentials


_config_instance: WeckPiConfig | None = None


def config() -> WeckPiConfig:
    """Get the configuration object."""
    global _config_instance
    if _config_instance is None:
        _config_instance = WeckPiConfig(Path())
    return _config_instance
