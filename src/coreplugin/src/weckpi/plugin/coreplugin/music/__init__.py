"""
This plugin package adds functionality to the WeckPi music system by adding:

- A media player based on the libMPV binding python-mpv
- A media provider for local music files
- A media provider for the streaming service TIDAL
"""
from .media_players.mpv import Mpv
from .media_providers.local_fs import LocalFS
from .media_providers.tidal import Tidal
