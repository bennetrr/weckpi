"""The main script of the WeckPi project."""
from __future__ import annotations

import importlib
import logging
import pkgutil
from dataclasses import asdict
from pathlib import Path
import sys
from typing import Any

import socketio
from flask import Flask

import weckpi.plugin
from weckpi.api.music import MediaPlayer, MediaProvider
from weckpi.api.plugin_manager import plugin_manager
from weckpi.api.config import config

root_logger = logging.getLogger('weckpi')
root_logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[{asctime} | {name} | {levelname}] {message}', '%H:%M:%S', style='{')
handler.setFormatter(formatter)

root_logger.addHandler(handler)

logger = logging.getLogger('weckpi.core.main')
sio_logger = logging.getLogger('weckpi.core.main.socket')


# TODO Unit / integration testing
# TODO Split into submodules
# TODO Implement settings and music selector

def main():
    """The main method of the main script of the WeckPi project."""
    sio = socketio.Server(
        async_mode='threading',
        logger=sio_logger,
        engineio_logger=sio_logger,
        cors_allowed_origins='*',  # TODO Change for security
    )
    app = Flask(__name__)
    app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

    def iter_namespace(ns_pkg: Any):
        # Specifying the second argument (prefix) to iter_modules makes the
        # returned name an absolute name instead of a relative one. This allows
        # import_module to work without having to do additional modification to
        # the name.
        return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

    discovered_plugins = {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in iter_namespace(weckpi.plugin)
    }

    for _, plugin_module in discovered_plugins.items():
        plugin_module.init()

    logger.info('Found %s plugins: %s', len(discovered_plugins), discovered_plugins)

    player: MediaPlayer = plugin_manager().get_media_player('mpv').cls()
    local_fs: MediaProvider = (plugin_manager().get_media_provider('localFs')
                               .cls(album_cover_dir=Path('./tmp-static/local-fs')))
    plugin_manager().get_media_provider('localFs').register_instance('localFs', local_fs)

    playlist = [
        'local-fs:local-fs:/Users/wemogymac/Music/VNV Nation/Transnational/04 Retaliate.wma',
        'local-fs:local-fs:/Users/wemogymac/Music/VNV Nation/Transnational/05 Lost Horizon.wma',
        'local-fs:local-fs:/Users/wemogymac/Music/VNV Nation/Transnational/07 If I Was.wma',
        'local-fs:local-fs:/Users/wemogymac/Music/VNV Nation/Transnational/08 Aeroscope.wma',
        'local-fs:local-fs:/Users/wemogymac/Music/VNV Nation/Transnational/09 Off Screen.wma'
    ]
    player.add_items(playlist)

    @sio.on('connect')
    def on_connect(sid, environ, auth):
        logger.info('Client connected with SID %s, env %s and auth %s', sid, environ, auth)

    @sio.on('disconnect')
    def on_disconnect(sid):
        logger.info('Client %s disconnected', sid)

    @sio.on('initialDataRequest')
    def on_initial_data_request(sid):
        logger.info('Client %s requested initial data', sid)
        player.play()
        player.volume = 60

        data = {
            'music': {
                'queue': [asdict(x) for x in player.queue],
                'queuePosition': player.queue_position,
                'isPlaying': True,
                'shuffle': player.shuffle,
                'repeat': player.repeat,
                'volume': player.volume,
                'position': player.position
            },
            'config': config().to_json()
        }

        logger.debug(data)

        return data

    @sio.on('propertyChange')
    def on_property_change(sid, data: dict):
        prop, value = data.get('prop'), data.get('value')
        logger.info('Client %s changed property %s to %s', sid, prop, value)

        match prop:
            case 'music.queuePosition':
                player.queue_position = value
            case 'music.position':
                player.position = value
            case 'music.isPlaying':
                if value:
                    player.play()
                else:
                    player.pause()
            case 'music.shuffle':
                player.shuffle = value
            case 'music.repeat':
                player.repeat = value
            case 'music.volume':
                player.volume = value

    @sio.on('action')
    def on_action(sid, data: dict):
        action = data.get('name')
        logger.info('Client %s activated action %s', sid, action)

        match action:
            case 'music.nextSong':
                player.next()
            case 'music.previousSong':
                player.previous()
            case 'music.stop':
                player.stop()

    player.on_queue_position_change = lambda value: sio.emit(
        'propertyChange',
        {'prop': 'music.queuePosition', 'value': value}
    )

    player.on_position_change = lambda value: sio.emit(
        'propertyChange',
        {'prop': 'music.position', 'value': value}
    )

    app.run()


if __name__ == '__main__':
    main()
