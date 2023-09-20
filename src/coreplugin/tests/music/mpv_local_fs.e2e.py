"""
End-to-end test for the mpv player and the localFs media provider.

This test is supposed to be run with PyCharm's interactive python console,
so you can control the player by invoking functions.
"""
from __future__ import annotations

import logging
from pathlib import Path

from weckpi.api.plugin_manager import plugin_manager
from weckpi.plugin.coreplugin.music.media_players.mpv import Mpv
from weckpi.plugin.coreplugin.music.media_providers.local_fs import LocalFS

logging.root.setLevel(logging.DEBUG)

plugin_manager().register_media_player('mpv', Mpv)
plugin_manager().register_media_provider('localFs', LocalFS, False, False, True)
plugin_manager().get_media_provider('localFs').register_instance('localFs', LocalFS(Path("/tmp/weckpi/localFs")))

playlist = [
    'localFs:localFs:/Users/wemogymac/Music/VNV Nation/Transnational/04 Retaliate.wma',
    'localFs:localFs:/Users/wemogymac/Music/VNV Nation/Transnational/05 Lost Horizon.wma',
    'localFs:localFs:/Users/wemogymac/Music/VNV Nation/Transnational/07 If I Was.wma',
    'localFs:localFs:/Users/wemogymac/Music/VNV Nation/Transnational/08 Aeroscope.wma',
    'localFs:localFs:/Users/wemogymac/Music/VNV Nation/Transnational/09 Off Screen.wma'
]

player = Mpv()
player.add_items(playlist)
