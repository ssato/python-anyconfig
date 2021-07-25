#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Utility funtions for anyconfig.ionfo.
"""
import pathlib
import typing

from .constants import (
    GLOB_MARKER, PATH_SEP, SPLIT_PATH_RE
)


def is_io_stream(obj: typing.Any) -> bool:
    """Is given object ``obj`` an IO stream, file or file-like object?
    """
    return callable(getattr(obj, 'read', False))


def get_path_and_ext(path: pathlib.Path) -> typing.Tuple[pathlib.Path, str]:
    """Normaliez path objects and retunr it with file extension.
    """
    abs_path = path.expanduser().resolve()
    file_ext = abs_path.suffix
    return (
        abs_path,
        file_ext[1:] if file_ext.startswith('.') else ''
    )


def split_path_by_marker(path: str,
                         marker: str = GLOB_MARKER,
                         path_sep: str = PATH_SEP,
                         split_re: typing.Pattern = SPLIT_PATH_RE
                         ) -> typing.Tuple[str, str]:
    """Split given path string by the marker.
    """
    if marker not in path:
        return (path, '')

    if path_sep not in path:
        return ('', path)

    matched = split_re.match(path)
    if not matched:
        raise ValueError(f'Invalid path: {path}')

    return typing.cast(typing.Tuple[str, str], matched.groups())

# vim:sw=4:ts=4:et:
