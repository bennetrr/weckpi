"""
End-to-end test for the mpv player and the local-fs media provider.

This test is supposed to be run with PyCharm's interactive python console,
so you can control the player by invoking functions.
"""
from __future__ import annotations

import logging

from weckpi.api.authentication import OAuthSession
from weckpi.api.plugin_manager import plugin_manager
from weckpi.plugin.coreplugin.music import Mpv, Tidal

logging.root.setLevel(logging.DEBUG)

plugin_manager().register_media_player('mpv', Mpv)
plugin_manager().register_media_provider('tidal', Tidal, True, True, True)

tidal = Tidal('demo')

plugin_manager().get_media_provider('tidal').register_instance('demo', tidal)

tidal.login(
    OAuthSession(
        'Bearer',
        'eyJraWQiOiJ2OU1GbFhqWSIsImFsZyI6IkVTMjU2In0.eyJ0eXBlIjoibzJfYWNjZXNzIiwidWlkIjoxNzg2NDA0ODUsInNjb3BlIjoid19zdWIgcl91c3Igd191c3IiLCJnVmVyIjowLCJzVmVyIjowLCJjaWQiOjMyMzUsImV4cCI6MTY5MTUwMjI1OSwic2lkIjoiNmQwZTVhZTEtMmM3Zi00MDIzLWE2MzQtZjc2YzE0NDI5MmI2IiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnRpZGFsLmNvbS92MSJ9.JgcNxbTbSiA9Wz6pkUAb0FjosJRfO9ceHm-E-TMOUymjH2AaftmVmSZcw6AVIGew5Z0iiqoYSBCU6sQjZcgsnw',
        'eyJraWQiOiJoUzFKYTdVMCIsImFsZyI6IkVTNTEyIn0.eyJ0eXBlIjoibzJfcmVmcmVzaCIsInVpZCI6MTc4NjQwNDg1LCJzY29wZSI6Indfc3ViIHJfdXNyIHdfdXNyIiwiY2lkIjozMjM1LCJzVmVyIjowLCJnVmVyIjowLCJpc3MiOiJodHRwczovL2F1dGgudGlkYWwuY29tL3YxIn0.AAkE5l_jm2eQwiO_tp0XSQ2BO3zSqcz-O1qoOCpxV4WkC3G43vs5uoAjYgVAa45p8igfuk5FnO_qtD0c4gQaU-6wAWbnlVEqZjfTlzZdgbp95QID3ZD8IKEokgc2FZPapWmRQo-u_NsVeiBQIZoU4ghfixnupDlp4aFOjmmknFQZQyFh',
        None
    )
)

playlist = [x.mrid for x in tidal.explore('tidal:demo:playlist:1d29d167-e5e1-4c68-b1b4-05d08f65bf43')]

player = Mpv()
player.add_items(playlist)
player.shuffle = True
