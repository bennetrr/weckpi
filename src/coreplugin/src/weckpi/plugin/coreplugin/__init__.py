"""
The WeckPi core plugin, which adds functionality to many of the features of the WeckPi.

See the documentation of the subpackages in this package for more information.
"""
from __future__ import annotations

from weckpi.api.plugin_manager import plugin_manager
from weckpi.plugin.coreplugin.music import LocalFS, Mpv, Tidal


def init():
    """Register the plugins classes."""
    # Music
    plugin_manager().register_media_player('mpv', Mpv)
    plugin_manager().register_media_provider(
        'localFs', LocalFS,
        needs_login=False, has_search=False, has_explore=True
    )
    plugin_manager().register_media_provider(
        'tidal', Tidal,
        needs_login=True, has_search=True, has_explore=True
    )
