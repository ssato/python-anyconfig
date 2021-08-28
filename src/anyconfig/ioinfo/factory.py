#
# Copyright (C) 2018 - 2021 Satoru SATOH <satoru.satoh @ gmmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
r"""ioinfo.main to provide internal APIs used from other modules.
"""
import pathlib
import typing

from .. import common
from . import utils


def from_path_object(path: pathlib.Path) -> common.IOInfo:
    """
    Return an IOInfo object made from :class:`pathlib.Path` object ``path``.
    """
    (abs_path, file_ext) = utils.get_path_and_ext(path)

    return common.IOInfo(
        abs_path, common.IOI_PATH_OBJ, str(abs_path), file_ext
    )


def from_io_stream(strm: typing.IO) -> common.IOInfo:
    """
    Return an IOInfo object made from IO stream object ``strm``.
    """
    path = getattr(strm, 'name', '')
    if path:
        (abs_path, file_ext) = utils.get_path_and_ext(pathlib.Path(path))
    else:
        (abs_path, file_ext) = (path, '')

    return common.IOInfo(
        strm, common.IOI_STREAM, str(abs_path), file_ext
    )


def make(obj: typing.Any) -> common.IOInfo:
    """
    :param obj: a path string, a pathlib.Path or a file / file-like object
    :return:
        Namedtuple object represents a kind of input object such as a file /
        file-like object, path string or pathlib.Path object

    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    if isinstance(obj, common.IOInfo):
        return obj

    if isinstance(obj, str):
        obj = pathlib.Path(obj)

    if isinstance(obj, pathlib.Path):
        return from_path_object(obj)

    # Which is better? isinstance(obj, io.IOBase):
    if getattr(obj, 'read', False):
        return from_io_stream(obj)

    raise ValueError(repr(obj))

# vim:sw=4:ts=4:et:
