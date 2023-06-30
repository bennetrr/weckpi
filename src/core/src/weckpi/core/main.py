from __future__ import annotations

import logging
import sys

import socketio
import eventlet.wsgi

root_logger = logging.getLogger('weckpi')
root_logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[{asctime} | {name} | {levelname}] {message}', '%H:%M:%S', style='{')
handler.setFormatter(formatter)

root_logger.addHandler(handler)

logger = logging.getLogger('weckpi.core.main')
sio_logger = logging.getLogger('weckpi.core.main.socket')


def main():
    sio = socketio.Server(
        async_mode='eventlet',
        logger=sio_logger,
        engineio_logger=sio_logger,
        cors_allowed_origins='*'  # TODO Change for security
    )

    @sio.on('connect')
    def on_connect(sid, environ, auth):
        logger.info('Client connected with SID %s, env %s and auth %s', sid, environ, auth)

    @sio.on('disconnect')
    def on_disconnect(sid):
        logger.info('Client %s disconnected', sid)

    @sio.on('initial-data-request')
    def on_initial_data_request(sid):
        logger.info('Client %s requested initial data', sid)

        return {
            'music': {
                'metadata': {
                    'title': 'Beloved',
                    'artist': 'VNV Nation',
                    'album': 'Futureperfect',
                    'image_uri': 'https://resources.tidal.com/images/2a85ef7a/1aef/43cc/8d2f/e9911c757c1a/1280x1280.jpg',
                    'duration': 7 + 24 / 60
                },
                'position': 1.20,
                'playing': True,
                'shuffle': True,
                'repeat': False,
                'volume': 50
            }
        }

    @sio.on('property-change')
    def on_property_change(sid, data: dict):
        prop, value = data.get('prop'), data.get('value')
        logger.info('Client %s changed property %s to %s', sid, prop, value)

    @sio.on('action')
    def on_action(sid, data: dict):
        action = data.get('name')
        logger.info('Client %s activated action %s', sid, action)

    app = socketio.WSGIApp(sio)
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)


if __name__ == '__main__':
    main()
