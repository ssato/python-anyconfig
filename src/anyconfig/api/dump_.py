#
# Copyright (C) 2012 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=unused-import,import-error,invalid-name
r"""Public APIs to dump configurations data.
"""
from ..common import PathOrIOInfoT, InDataExT
from ..ioinfo import make as ioinfo_make
from ..parsers import find, MaybeParserT
from .datatypes import ParserT


def dump(data: InDataExT, out: PathOrIOInfoT,
         ac_parser: MaybeParserT = None, **options) -> None:
    """
    Save 'data' to 'out'.

    :param data: A mapping object may have configurations data to dump
    :param out:
        An output file path, a file, a file-like object, :class:`pathlib.Path`
        object represents the file or a namedtuple 'anyconfig.common.IOInfo'
        object represents output to dump some data to.
    :param ac_parser: Forced parser type or parser object
    :param options:
        Backend specific optional arguments, e.g. {"indent": 2} for JSON
        loader/dumper backend

    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    ioi = ioinfo_make(out)
    psr: ParserT = find(ioi, forced_type=ac_parser)
    psr.dump(data, ioi, **options)


def dumps(data: InDataExT, ac_parser: MaybeParserT = None,
          **options) -> str:
    """
    Return string representation of 'data' in forced type format.

    :param data: Config data object to dump
    :param ac_parser: Forced parser type or ID or parser object
    :param options: see :func:`dump`

    :return: Backend-specific string representation for the given data
    :raises: ValueError, UnknownProcessorTypeError
    """
    psr: ParserT = find(None, forced_type=ac_parser)
    return psr.dumps(data, **options)

# vim:sw=4:ts=4:et:
