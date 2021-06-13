#
# Copyright (C) 2012 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
r"""A Public API to open configuration files by detecting type automatically.
"""
import typing
import warnings

from ..common import PathOrIOInfoT, IOI_STREAM
from ..ioinfo import make as ioinfo_make
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
    if not path:
        raise ValueError(f'Invalid argument, path: {path!r}')

    ioi = ioinfo_make(path)
    if ioi.type == IOI_STREAM:
        warnings.warn(f'Looks already opened stream: {ioi!r}')
        return typing.cast(typing.IO, ioi.src)

    psr: ParserT = find(ioi, forced_type=ac_parser)

    if mode is not None and mode.startswith('w'):
        return psr.wopen(ioi.path, **options)

    return psr.ropen(ioi.path, **options)

# vim:sw=4:ts=4:et:
