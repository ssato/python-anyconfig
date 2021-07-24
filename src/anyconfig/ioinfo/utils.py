#
# Copyright (C) 2018 - 2021 Satoru SATOH <satoru.satoh @ gmmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
r"""ioinfo.utils - provides utility functions for internal use.
"""
import pathlib
import typing

from ..common import (
    IOI_PATH_STR, IOI_PATH_OBJ, IOI_STREAM,
    UnknownFileTypeError
)
from ..utils import (
    is_path, is_path_obj, is_file_stream,
    get_path_from_stream, get_file_extension
)


IoiTypeT = str


def guess_io_type(obj: typing.Any) -> IoiTypeT:
    """Guess input or output type of 'obj'.

    :return: IOInfo type defined in anyconfig.common.IOI_TYPES
    """
    if is_path(obj):
        return IOI_PATH_STR
    if is_path_obj(obj):
        return IOI_PATH_OBJ
    if is_file_stream(obj):
        return IOI_STREAM

    raise ValueError(f'Unknown I/O type object: {obj!r}')


MaybeIoObjT = typing.Union[pathlib.Path, typing.IO, typing.Any]


def inspect_io_obj(obj: MaybeIoObjT, itype: IoiTypeT
                   ) -> typing.Tuple[str, str]:
    """
    Inspect given object ``obj`` and return it with necessary attributes are
    set if it is one of pathlib.Path or a stream (file or file-like object), or
    raise :class:`UnknownFileTypeError`

    :param obj: It should be a pathlib.Path or a file / file-like object

    :return: A tuple of (filepath, fileext)
    """
    if itype == IOI_PATH_OBJ:
        path = typing.cast(pathlib.Path, obj).expanduser().resolve()

        ipath = str(path)
        ext = path.suffix[1:]

    elif itype == IOI_STREAM:
        ipath = get_path_from_stream(typing.cast(typing.IO, obj)) or ''
        ext = get_file_extension(ipath) if ipath else ''

    else:
        raise UnknownFileTypeError(repr(obj))

    return (ipath, ext)

# vim:sw=4:ts=4:et:
