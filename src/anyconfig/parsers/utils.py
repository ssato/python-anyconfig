#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=unused-import,import-error,invalid-name
r"""Internal APIs to load, list and find parser class objects.
"""
import typing

from ..common import PathOrIOInfoT
from ..backend import ParserT, ParsersT
from .parsers import Parsers


ParserClssT = typing.List[typing.Type[ParserT]]


def load_plugins() -> None:
    """[Re-]Load pluggable processors.
    """
    Parsers().load_plugins()


def list_types() -> typing.List[str]:
    """List supported processor types.
    """
    return sorted(Parsers().list_x('type'))


def list_by_cid() -> typing.List[typing.Tuple[str, ParserClssT]]:
    """
    List processors by each cid, [(cid, [Parser_class])].
    """
    return Parsers().list_by_x('cid')


def list_by_type() -> typing.List[typing.Tuple[str, ParserClssT]]:
    """
    List processor by eacch type, [(type, [Parser_class])].
    """
    return Parsers().list_by_x('type')


def list_by_extension() -> typing.List[typing.Tuple[str, ParserClssT]]:
    """
    List processor by file extension supported, [(extension, [Parser_class])].
    """
    return Parsers().list_by_x('extensions')


def findall(obj: typing.Optional[PathOrIOInfoT] = None,
            forced_type: typing.Optional[str] = None
            ) -> ParsersT:
    """
    Find out processor objects can process data from given 'obj' which may be a
    file path, file or file-like object, pathlib.Path object or an
    'anyconfig.common.IOInfo' (namedtuple) object.

    :param obj:
        a file path, file or file-like object, pathlib.Path object, an
        'anyconfig.common.IOInfo' (namedtuple) object, or None
    :param forced_type: Forced type or id of the processor

    :return: A list of instances of processor classes to process 'obj'
    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    return Parsers().findall(obj, forced_type=forced_type)


def find(obj: typing.Optional[PathOrIOInfoT] = None,
         forced_type: typing.Optional[str] = None) -> ParserT:
    """
    This function is very similar to the above :func:`findall` but returns
    *a processor object* instead of a list of processor objects.

    :param obj:
        a file path, file or file-like object, pathlib.Path object, an
        'anyconfig.common.IOInfo' (namedtuple) object, or None
    :param forced_type: Forced type or id of the processor

    :return:
        An instance of processor class of highest priority to process 'obj'
    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    return Parsers().find(obj, forced_type=forced_type)

# vim:sw=4:ts=4:et:
