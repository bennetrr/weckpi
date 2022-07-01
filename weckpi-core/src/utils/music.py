"""Utilitys for the music module"""
from music.tidal.tidal_session import TidalSession


def add_vlc_argument(args: tuple[str], arg: str) -> tuple[str]:
    """
    Add a new argument to the list of arguments

    :param args: The old list of arguments
    :param arg: The new argument
    :return: The new list of arguments
    """
    if arg in args:
        return args
    list_args = list(args)
    list_args.append(arg)
    return tuple(list_args)


def get_mrl(uid: str, tidal_session: TidalSession = None):
    """
    Get the MRL for a given ID or URL.
    There are a few formats of IDs:

    * ``tidal+<type>+<id>`` where ``<type>`` is one of ``track``, ``album``, ``artist``, ``playlist``.
      These IDs are created by the TIDAL API wrapper.
      They can only be processed if ``tidal_session`` is a valid session.
    * Every other string is interpreted as a VLC-compatible MRL.
    """
    if uid.startswith('tidal+'):
        if tidal_session is None:
            raise ValueError('TIDAL IDs can only be processed if a valid TIDAL session is provided')
        return tidal_session.resolve_id(uid).get_url()
