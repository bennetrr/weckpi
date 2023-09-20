"""
End-to-end test for the mpv player and the local-fs media provider.

This test is supposed to be run with PyCharm's interactive python console,
so you can control the player by invoking functions.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

from weckpi.api.authentication import OAuthSession
from weckpi.api.plugin_manager import plugin_manager
from weckpi.plugin.coreplugin.music import Mpv, Tidal

logging.root.setLevel(logging.DEBUG)

plugin_manager().register_media_player('mpv', Mpv)
plugin_manager().register_media_provider('tidal', Tidal, True, True, True)

tidal = Tidal('demo')

plugin_manager().get_media_provider('tidal').register_instance('demo', tidal)

with Path('tidal.secret.json').open('r', encoding='utf-8') as secret_file:
    secret_json = json.load(secret_file)

tidal.login(
    OAuthSession(
        secret_json['authSession']['tokenType'],
        secret_json['authSession']['accessToken'],
        secret_json['authSession']['refreshToken'],
        datetime.fromisoformat(secret_json['authSession']['expireTime'])
    )
)

playlist = [x.mrid for x in tidal.explore('tidal:demo:playlist:1d29d167-e5e1-4c68-b1b4-05d08f65bf43')]

player = Mpv()
player.add_items(playlist)
player.shuffle = True
tidal.search('VNV Nation')
