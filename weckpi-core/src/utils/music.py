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


def get_mrl(uri: str, tidal_session: TidalSession = None) -> str:
    """
    Get the MRL for the given URI.

    There are a few formats of URIs:

    * ``tidal:<type>:<id>`` where ``<type>`` is one of ``track``, ``album``, ``artist``, ``playlist``.
      These URIs are produced by the TIDAL API wrapper.
      They can only be processed if ``tidal_session`` is a valid session.
    * Every other string is interpreted as a VLC-compatible MRL.
    """
    if uri.startswith('tidal:'):
        if tidal_session is None:
            raise ValueError('TIDAL IDs can only be processed if a valid TIDAL session is provided')
        obj = tidal_session.resolve_uri(uri)
        mrl = tidal_session.get_mrl(obj)

    else:
        mrl = uri

    return mrl
