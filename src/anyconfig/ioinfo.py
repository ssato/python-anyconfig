#
# Copyright (C) 2018 Satoru SATOH <ssato @ redhat.com>
# Copyright (C) 2019 - 2020 Satoru SATOH <satoru.satoh @ gmmail.com>
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
from __future__ import absolute_import

import pathlib

import anyconfig.utils

from anyconfig.globals import (
    IOInfo, IOI_NONE, IOI_PATH_STR, IOI_PATH_OBJ, IOI_STREAM,
    UnknownFileTypeError
)


def guess_io_type(obj):
    """Guess input or output type of 'obj'.

    :param obj: a path string, a pathlib.Path or a file / file-like object
    :return: IOInfo type defined in anyconfig.globals.IOI_TYPES

    >>> apath = "/path/to/a_conf.ext"
    >>> assert guess_io_type(apath) == IOI_PATH_STR
    >>> assert guess_io_type(pathlib.Path(apath)) == IOI_PATH_OBJ
    >>> assert guess_io_type(open(__file__)) == IOI_STREAM
    >>> guess_io_type(1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: ...
    """
    if obj is None:
        return IOI_NONE
    if anyconfig.utils.is_path(obj):
        return IOI_PATH_STR
    if anyconfig.utils.is_path_obj(obj):
        return IOI_PATH_OBJ
    if anyconfig.utils.is_file_stream(obj):
        return IOI_STREAM

    raise ValueError("Unknown I/O type object: {!r}".format(obj))


def inspect_io_obj(obj, itype):
    """
    :param obj: a path string, a pathlib.Path or a file / file-like object

    :return: A tuple of (filepath, fileext)
    :raises: UnknownFileTypeError
    """
    if itype == IOI_PATH_OBJ:
        path = obj.expanduser().resolve()

        ipath = str(path)
        ext = path.suffix[1:]

    elif itype == IOI_STREAM:
        ipath = anyconfig.utils.get_path_from_stream(obj)
        ext = anyconfig.utils.get_file_extension(ipath) if ipath else None

    elif itype == IOI_NONE:
        ipath = ext = None
    else:
        raise UnknownFileTypeError("%r" % obj)

    return (ipath, ext)


def make(obj):
    """
    :param obj: a path string, a pathlib.Path or a file / file-like object
    :return:
        Namedtuple object represents a kind of input object such as a file /
        file-like object, path string or pathlib.Path object

    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    if anyconfig.utils.is_ioinfo(obj):
        return obj

    itype = guess_io_type(obj)

    if itype == IOI_PATH_STR:
        obj = pathlib.Path(obj)
        itype = IOI_PATH_OBJ

    (ipath, ext) = inspect_io_obj(obj, itype)
    return IOInfo(src=obj, type=itype, path=ipath, extension=ext)

# vim:sw=4:ts=4:et:
