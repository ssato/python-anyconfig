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
from . import detectors, utils


GLOB_MARKER: str = '*'


def from_path_object(path: pathlib.Path) -> common.IOInfo:
    """
    Return an IOInfo object made from :class:`pathlib.Path` object ``path``.
    """
    (abs_path, file_ext) = utils.get_path_and_ext(path)

    return common.IOInfo(
        abs_path, common.IOI_PATH_OBJ, str(abs_path), file_ext
    )


def from_path_str(path: str) -> common.IOInfo:
    """Return an IOInfo object made from a str ``path``.
    """
    return from_path_object(pathlib.Path(path).resolve())


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
    """Make and return a :class:`common.IOInfo` object from object ``obj``.
    """
    if isinstance(obj, common.IOInfo):
        return obj

    if isinstance(obj, str):
        return from_path_str(obj)

    if isinstance(obj, pathlib.Path):
        return from_path_object(obj)

    # Which is better? isinstance(obj, io.IOBase):
    if getattr(obj, 'read', False):
        return from_io_stream(obj)

    raise ValueError(repr(obj))


def expand_from_path(path: pathlib.Path) -> typing.Iterator[pathlib.Path]:
    """
    Expand given path ``path`` contains '*' in its path str and yield
    :class:`pathlib.Path` objects.
    """
    (base, pattern) = utils.split_path_by_marker(str(path))

    if pattern:
        base_2 = pathlib.Path(base or '.').resolve()
        for path_2 in sorted(base_2.glob(pattern)):
            yield path_2
    else:
        yield pathlib.Path(base)


def make_itr(obj: typing.Any, marker: str = GLOB_MARKER
             ) -> typing.Iterator[common.IOInfo]:
    """Make and yield a series of :class:`common.IOInfo` objects.
    """
    if isinstance(obj, common.IOInfo):
        yield obj

    elif detectors.is_path_str(obj):
        for path in expand_from_path(pathlib.Path(obj)):
            yield from_path_object(path)

    elif detectors.is_path_obj(obj):
        for path in expand_from_path(obj):
            yield from_path_object(path)

    elif detectors.is_io_stream(obj):
        yield from_io_stream(obj)

    else:
        for item in obj:
            for ioi in make_itr(item, marker=marker):
                yield ioi

# vim:sw=4:ts=4:et:
