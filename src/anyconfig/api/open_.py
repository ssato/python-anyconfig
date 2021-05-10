#
# Copyright (C) 2012 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
r"""A Public API to open configuration files by detecting type automatically.
"""
import typing

from ..common import PathOrIOInfoT
from ..parsers import find, MaybeParserT
from .datatypes import ParserT


# pylint: disable=redefined-builtin
def open(path: PathOrIOInfoT, mode: typing.Optional[str] = None,
         ac_parser: MaybeParserT = None, **options) -> typing.IO:
    """
    Open given configuration file with appropriate open flag.

    :param path: Configuration file path
    :param mode:
        Can be 'r' and 'rb' for reading (default) or 'w', 'wb' for writing.
        Please note that even if you specify 'r' or 'w', it will be changed to
        'rb' or 'wb' if selected backend, xml and configobj for example, for
        given config file prefer that.
    :param options:
        Optional keyword arguments passed to the internal file opening APIs of
        each backends such like 'buffering' optional parameter passed to
        builtin 'open' function.

    :return: A file object or None on any errors
    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    psr: ParserT = find(path, forced_type=ac_parser)

    if mode is not None and mode.startswith('w'):
        return psr.wopen(path, **options)

    return psr.ropen(path, **options)

# vim:sw=4:ts=4:et:
