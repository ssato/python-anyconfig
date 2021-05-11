#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Utility funtions to process file and file paths.
"""
import functools
import operator
import os.path
import os
import re
import pathlib
import typing

from ..common import (
    IOInfo, PathOrIOInfoT
)
from .detectors import (
    is_file_stream, is_ioinfo
)
from ..ioinfo import make as ioinfo_make


GLOB_MARKER = '*'


def get_file_extension(file_path: str) -> str:
    """
    Get file extension from the path `file_path`.
    """
    default = ''

    if not file_path:
        return default

    _ext = os.path.splitext(file_path)[-1]
    if _ext:
        return _ext[1:] if _ext.startswith('.') else _ext

    return default


def get_path_from_stream(strm: typing.IO, safe: bool = False) -> str:
    """
    Try to get file path from given file or file-like object 'strm'.

    :param strm: A file or file-like object might have its file path info
    :return: file path or None
    :raises: ValueError
    """
    if not is_file_stream(strm) and not safe:
        raise ValueError(f'It does not look a file[-like] object: {strm!r}')

    path = getattr(strm, 'name', None)
    if path is not None:
        try:
            return str(pathlib.Path(path).resolve())
        except (TypeError, ValueError):
            pass

    return ''


@functools.lru_cache()
def split_re(marker: str, sep: str = os.path.sep) -> typing.Pattern:
    """Generate a regexp pattern object to split path by marker.
    """
    return re.compile(r'([^{0}]+){1}(.*\{0}.*)'.format(marker, sep))


def split_path_by_marker(path: str, marker: str = GLOB_MARKER,
                         sep: str = os.path.sep
                         ) -> typing.Tuple[str, str]:
    """
    Split given path string by the marker.

    >>> split_path_by_marker('a.txt')
    ('a.txt', '')
    >>> split_path_by_marker('*.txt')
    ('', '*.txt')
    >>> split_path_by_marker('a/*.txt')
    ('a', '*.txt')
    >>> split_path_by_marker('a/b/*.txt')
    ('a/b', '*.txt')
    >>> split_path_by_marker('a/b/*/*.txt')
    ('a/b', '*/*.txt')
    """
    if marker not in path:
        return (path, '')

    if sep not in path:
        return ('', path)

    matched = split_re(marker, sep=sep).match(path)
    if not matched:
        raise ValueError(f'Invalid path: {path}')

    return typing.cast(typing.Tuple[str, str], matched.groups())


PathOrIO = typing.Union[pathlib.Path, typing.IO]


def expand_paths_itr(paths: typing.Union[PathOrIOInfoT,
                                         typing.List[PathOrIOInfoT]],
                     marker: str = GLOB_MARKER
                     ) -> typing.Iterator[IOInfo]:
    """
    :param paths:
        A glob path pattern string or pathlib.Path object holding such path, or
        a list consists of path strings or glob path pattern strings or
        pathlib.Path object holding such ones.

    :param marker: A character or string to globbing paths
    """
    if isinstance(paths, (str, pathlib.Path)):
        if isinstance(paths, pathlib.Path):
            paths = str(paths)

        (base, pattern) = split_path_by_marker(paths, marker=marker)

        if not pattern:
            yield ioinfo_make(pathlib.Path(base))
            return

        base_2 = pathlib.Path(os.curdir if not base else base).resolve()
        for path in sorted(base_2.glob(pattern)):
            yield ioinfo_make(path)

    elif is_file_stream(paths):
        yield ioinfo_make(paths)

    elif is_ioinfo(paths):
        yield typing.cast(IOInfo, paths)

    else:
        for path in paths:  # type: ignore
            for cpath in expand_paths_itr(path, marker=marker):
                yield cpath


def expand_paths(paths: PathOrIOInfoT, marker: str = GLOB_MARKER
                 ) -> typing.Iterable[IOInfo]:
    """
    :param paths:
        A glob path pattern string or pathlib.Path object holding such path, or
        a list consists of path strings or glob path pattern strings or
        pathlib.Path object holding such ones, or file objects
    :param marker: Glob marker character or string, e.g. '*'
    """
    return sorted(
        expand_paths_itr(paths, marker=marker),
        key=operator.attrgetter('path')
    )


def _try_to_get_extension(obj: PathOrIO) -> typing.Optional[str]:
    """
    Try to get file extension from given path or file object.

    :param obj: a file, file-like object or something
    :return: File extension or None

    >>> path = pathlib.Path(__file__)
    >>> _try_to_get_extension(path)
    'py'
    >>> with path.open() as fio:
    ...     _try_to_get_extension(fio)
    'py'
    """
    if isinstance(obj, pathlib.Path):
        return obj.suffix[1:]

    path = get_path_from_stream(obj, safe=True)
    if path is None:
        return None

    return _try_to_get_extension(pathlib.Path(path))


def are_same_file_types(objs: typing.List[PathOrIO]) -> bool:
    """
    Are given objects, pathlib.Path or io, same type (have same extension)?
    """
    if not objs:
        return False

    ext = _try_to_get_extension(objs[0])
    if ext is None:
        return False

    return all(_try_to_get_extension(p) == ext for p in objs[1:])

# vim:sw=4:ts=4:et:
