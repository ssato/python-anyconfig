#
# Copyright (C) 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=invalid-name
r"""Functions for value objects represent inputs and outputs.

.. versionadded:: 0.9.5

- Add functions to make and process input and output object holding some
  attributes like input and output type (path, stream or pathlib.Path object),
  path, opener, etc.
"""
from __future__ import absolute_import
import anyconfig.utils

from anyconfig.globals import (
    IOInfo, IOI_NONE, IOI_PATH_STR, IOI_PATH_OBJ, IOI_STREAM,
    UnknownFileTypeError
)


def guess_io_type(obj):
    """Guess input or output type of ``obj``.

    :param obj: a path string, a pathlib.Path or a file / file-like object
    :return: IOInfo type defined in anyconfig.globals.IOI_TYPES

    >>> apath = "/path/to/a_conf.ext"
    >>> assert guess_io_type(apath) == IOI_PATH_STR

    >>> from anyconfig.compat import pathlib
    >>> if pathlib is not None:
    ...     assert guess_io_type(pathlib.Path(apath)) == IOI_PATH_OBJ
    >>> assert guess_io_type(open(__file__)) == IOI_STREAM
    """
    if obj is None:
        return IOI_NONE
    elif anyconfig.utils.is_path(obj):
        return IOI_PATH_STR
    elif anyconfig.utils.is_path_obj(obj):
        return IOI_PATH_OBJ

    return IOI_STREAM


def inspect_io_obj(obj):
    """
    :param obj: a path string, a pathlib.Path or a file / file-like object

    :return: A tuple of (objtype, objpath, objopener)
    :raises: UnknownFileTypeError
    """
    itype = guess_io_type(obj)

    if itype == IOI_PATH_STR:
        ipath = anyconfig.utils.normpath(obj)
        opener = open
    elif itype == IOI_PATH_OBJ:
        ipath = anyconfig.utils.normpath(obj.as_posix())
        opener = obj.open
    elif itype == IOI_STREAM:
        ipath = anyconfig.utils.get_path_from_stream(obj)
        opener = anyconfig.utils.noop
    elif itype == IOI_NONE:
        ipath = None
        opener = anyconfig.utils.noop
    else:
        raise UnknownFileTypeError("%r" % obj)

    return (itype, ipath, opener)


def make(obj, forced_type=None):
    """
    :param obj: a path string, a pathlib.Path or a file / file-like object
    :param prs: A list of processor classes
    :param forced_type: Forced processor type or processor object

    :return:
        Namedtuple object represents a kind of input object such as a file /
        file-like object, path string or pathlib.Path object

    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    if anyconfig.utils.is_ioinfo(obj):
        return obj

    if (obj is None or not obj) and forced_type is None:
        raise ValueError("obj or forced_type must be some value")

    (itype, ipath, opener) = inspect_io_obj(obj)
    return IOInfo(src=obj, type=itype, path=ipath, opener=opener)

# vim:sw=4:ts=4:et:
