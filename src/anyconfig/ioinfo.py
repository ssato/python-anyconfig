#
# Copyright (C) 2018 - 2020 Satoru SATOH <satoru.satoh @ gmmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
r"""Functions for value objects represent inputs and outputs.

.. versionchanged:: 0.10.1

- simplify inspect_io_obj and make; detect type in make, remove the member
  opener from ioinfo object, etc.

.. versionadded:: 0.9.5

- Add functions to make and process input and output object holding some
  attributes like input and output type (path, stream or pathlib.Path object),
  path, opener, etc.
"""
import pathlib
import typing

from .common import (
    IOInfo, IOI_PATH_STR, IOI_PATH_OBJ, IOI_STREAM,
    UnknownFileTypeError
)
from .utils import (
    is_path, is_path_obj, is_file_stream,
    get_path_from_stream, get_file_extension,
    is_ioinfo
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
        path = obj.expanduser().resolve()

        ipath = str(path)
        ext = path.suffix[1:]

    elif itype == IOI_STREAM:
        ipath = get_path_from_stream(obj) or ''
        ext = get_file_extension(ipath) if ipath else ''

    else:
        raise UnknownFileTypeError(repr(obj))

    return (ipath, ext)


def make(obj: typing.Any) -> IOInfo:
    """
    :param obj: a path string, a pathlib.Path or a file / file-like object
    :return:
        Namedtuple object represents a kind of input object such as a file /
        file-like object, path string or pathlib.Path object

    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    if is_ioinfo(obj):
        return obj

    itype = guess_io_type(obj)

    if itype == IOI_PATH_STR:
        obj = pathlib.Path(obj)
        itype = IOI_PATH_OBJ

    (ipath, ext) = inspect_io_obj(obj, itype)
    return IOInfo(src=obj, type=itype, path=ipath, extension=ext)

# vim:sw=4:ts=4:et:
