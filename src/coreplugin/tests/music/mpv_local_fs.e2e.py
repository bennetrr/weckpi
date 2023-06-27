"""
End-to-end test for the mpv player and the local-fs media provider.

This test is supposed to be run with PyCharm's interactive python console,
so you can control the player by invoking functions.
"""
from __future__ import annotations

import logging

from weckpi.api.plugin_manager import PluginManager

from weckpi.coreplugin.music.media_providers.local_fs import LocalFS
from weckpi.coreplugin.music.media_players.mpv import MpvMediaPlayer

logging.root.setLevel(logging.DEBUG)

PluginManager.get_instance().register_media_player('mpv', MpvMediaPlayer)
PluginManager.get_instance().register_media_provider('local-fs', LocalFS, False, False, True)
PluginManager.get_instance().get_media_provider('local-fs').register_instance('local-fs', LocalFS())

playlist = [
    'local-fs:local-fs:/Users/wemogymac/Music/VNV Nation/Transnational/04 Retaliate.wma',
    'local-fs:local-fs:/Users/wemogymac/Music/VNV Nation/Transnational/05 Lost Horizon.wma',
    'local-fs:local-fs:/Users/wemogymac/Music/VNV Nation/Transnational/07 If I Was.wma',
    'local-fs:local-fs:/Users/wemogymac/Music/VNV Nation/Transnational/08 Aeroscope.wma',
    'local-fs:local-fs:/Users/wemogymac/Music/VNV Nation/Transnational/09 Off Screen.wma'
]

player = MpvMediaPlayer()
player.add_media(playlist)
