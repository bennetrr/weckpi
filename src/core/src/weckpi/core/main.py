"""The main script of the WeckPi project."""
from __future__ import annotations

import importlib
import logging
import pkgutil
from dataclasses import asdict
from pathlib import Path
from typing import Any
from datetime import datetime, time
from threading import Thread
from time import sleep

import socketio
import sys
from flask import Flask

import weckpi.plugin
from weckpi.api.config import config
from weckpi.api.music import MediaPlayer, MediaProvider
from weckpi.api.plugin_manager import plugin_manager

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
    config(Path('../../../resources/test-config.secret.json'))

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
                               .cls(album_cover_dir=Path('/tmp/weckpi/localFs')))
    plugin_manager().get_media_provider('localFs').register_instance('localFs', local_fs)

    playlist = [
        'localFs:localFs:/Users/wemogymac/Music/VNV Nation/Transnational/04 Retaliate.wma',
        'localFs:localFs:/Users/wemogymac/Music/VNV Nation/Transnational/05 Lost Horizon.wma',
        'localFs:localFs:/Users/wemogymac/Music/VNV Nation/Transnational/07 If I Was.wma',
        'localFs:localFs:/Users/wemogymac/Music/VNV Nation/Transnational/08 Aeroscope.wma',
        'localFs:localFs:/Users/wemogymac/Music/VNV Nation/Transnational/09 Off Screen.wma'
    ]
    player.add_items(playlist)

    @sio.on('connect')
    def on_connect(sid, environ, auth):
        logger.info('Client connected with SID %s, env %s and auth %s', sid, environ, auth)

    @sio.on('disconnect')
    def on_disconnect(sid):
        logger.info('Client %s disconnected', sid)

    @sio.on('initialAppState')
    def on_initial_app_state_request(sid):
        logger.info('Client %s requested initial app state', sid)
        player.volume = 60

        data = {
            'music': {
                'queue': [asdict(x) for x in player.queue],
                'queuePosition': player.queue_position,
                'isPlaying': False,
                'shuffle': player.shuffle,
                'repeat': player.repeat,
                'volume': player.volume,
                'position': player.position
            },
            'initialized': True,
            'config': {
                'alarm': config().alarm.to_json()
            }
        }

        logger.debug(data)
        return data

    @sio.on('appStatePatch')
    def on_app_state_patch(sid, data: dict):
        path: str = data.get('path')
        value: Any = data.get('value')
        logger.info('Client %s changed property %s to %s', sid, path, value)

        if path.startswith('/config/alarm/'):
            _, _, _, weekday, prop = path.split('/')

            alarm_config = config().alarm.get_alarm_config(
                {'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7}
                [weekday]
            )

            match prop:
                case 'active':
                    alarm_config.active = value
                case 'time':
                    alarm_config.time = time.fromisoformat(value)
                case 'overrideActive':
                    alarm_config.override_active = value
                case 'overrideTime':
                    alarm_config.override_time = time.fromisoformat(value)
            config().flush()

        match path:
            case '/music/queuePosition':
                player.queue_position = value
            case '/music/position':
                player.position = value
            case '/music/isPlaying':
                if value:
                    player.play()
                else:
                    player.pause()
            case '/music/shuffle':
                player.shuffle = value
            case '/music/repeat':
                player.repeat = value
            case '/music/volume':
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
        'appStatePatch',
        {'prop': '/music/queuePosition', 'value': value}
    )

    player.on_position_change = lambda value: sio.emit(
        'appStatePatch',
        {'prop': '/music/position', 'value': value}
    )

    def get_next_alarm() -> dict[str, time] | None:
        current_weekday = datetime.now().isoweekday()
        current_time = datetime.now().time().replace(second=0, microsecond=0)

        weekdays = list(range(current_weekday, 8)) + list(range(1, current_weekday))

        logger.debug('currentTime=%s, currentWeekday=%s, weekdays=%s', current_time, current_weekday, weekdays)

        for weekday in weekdays:
            alarm_config = config().alarm.get_alarm_config(weekday)
            logger.debug("weekday=%s, alarmConfig=%s", weekday, alarm_config)

            if alarm_config.override_active and (
                    weekday != current_weekday or alarm_config.override_time >= current_time):
                return {"time": alarm_config.override_time, "weekday": weekday}

            if alarm_config.active and (weekday != current_weekday or alarm_config.time >= current_time):
                return {"time": alarm_config.time, "weekday": weekday}

        return None

    def t_alarm():
        alarm_active = False

        while True:
            sleep(10)
            # Get the next alarm
            next_alarm = get_next_alarm()
            logger.debug('Next alarm: %s, %s', next_alarm['weekday'], next_alarm['time'].isoformat())

            if next_alarm is None:
                continue

            if next_alarm['weekday'] == datetime.now().isoweekday() and \
               next_alarm['time'].hour == datetime.now().hour and \
               next_alarm['time'].minute == datetime.now().minute and \
               not alarm_active:
                alarm_active = True
                logger.info('Activated alarm!')
                player.play()
            if next_alarm['weekday'] == datetime.now().isoweekday() and \
               next_alarm['time'].hour == datetime.now().hour and \
               next_alarm['time'].minute + 1 == datetime.now().minute:
                alarm_active = False

    alarm_thread = Thread(target=t_alarm)
    alarm_thread.start()
    app.run()


if __name__ == '__main__':
    main()
