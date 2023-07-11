"""The WeckPi core plugin, that has all the default content for the WeckPi project."""
from __future__ import annotations

from weckpi.api.plugin_manager import plugin_manager

from weckpi.plugin.coreplugin.music import MpvMediaPlayer, Tidal, LocalFS


def init():
    """Register the plugin."""
    # Music
    plugin_manager().register_media_player('mpv', MpvMediaPlayer)
    plugin_manager().register_media_provider('local-fs', LocalFS, needs_login=False,has_search=False, has_explore=True)
    plugin_manager().register_media_provider('tidal', Tidal, needs_login=True, has_search=True, has_explore=True)
