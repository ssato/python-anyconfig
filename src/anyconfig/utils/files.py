#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Utility funtions to process file and file paths.
"""
import functools
import os.path
import os
import re
import pathlib
import typing

from ..common import (
    GLOB_MARKER, IOInfo, PathOrIOInfoT
)


def is_io_stream(obj: typing.Any) -> bool:
    """Is given object ``obj`` an IO stream, file or file-like object?
    """
    return callable(getattr(obj, 'read', False))


def get_path_from_stream(strm: typing.IO, safe: bool = False) -> str:
    """
    Try to get file path from given file or file-like object 'strm'.

    :param strm: A file or file-like object might have its file path info
    :return: file path or None
    :raises: ValueError
    """
    if not is_io_stream(strm) and not safe:
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


def expand_paths_itr(paths: typing.Union[typing.Iterable[PathOrIOInfoT],
                                         PathOrIOInfoT],
                     marker: str = GLOB_MARKER
                     ) -> typing.Iterator[PathOrIOInfoT]:
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
            yield pathlib.Path(base)
            return

        base_2 = pathlib.Path(os.curdir if not base else base).resolve()
        for path in sorted(base_2.glob(pattern)):
            yield path

    elif is_io_stream(paths):
        yield paths  # type: ignore

    elif isinstance(paths, IOInfo):
        yield typing.cast(IOInfo, paths)

    else:
        for path in paths:  # type: ignore
            for cpath in expand_paths_itr(path, marker=marker):
                yield cpath


def expand_paths(paths: typing.Union[typing.Iterable[PathOrIOInfoT],
                                     PathOrIOInfoT],
                 marker: str = GLOB_MARKER
                 ) -> typing.Iterable[PathOrIOInfoT]:
    """
    :param paths:
        A glob path pattern string or pathlib.Path object holding such path, or
        a list consists of path strings or glob path pattern strings or
        pathlib.Path object holding such ones, or file objects
    :param marker: Glob marker character or string, e.g. '*'
    """
    return list(expand_paths_itr(paths, marker=marker))

# vim:sw=4:ts=4:et:
