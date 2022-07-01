"""Utilitys for the music module"""


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
