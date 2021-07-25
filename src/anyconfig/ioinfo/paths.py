#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Utility funtions to process file and file paths.
"""
import pathlib
import typing

from ..common import (
    IOInfo, PathOrIOInfoT
)
from . import factory, utils


PathOrPathsT = typing.Union[
    typing.Iterable[PathOrIOInfoT],
    PathOrIOInfoT
]


def expand_paths_itr(paths: PathOrPathsT) -> typing.Iterator[PathOrIOInfoT]:
    """
    :param paths:
        A glob path pattern string or pathlib.Path object holding such path, or
        a list consists of path strings or glob path pattern strings or
        pathlib.Path object holding such ones.
    """
    if isinstance(paths, IOInfo):
        yield typing.cast(IOInfo, paths)

    elif isinstance(paths, (str, pathlib.Path)):
        if isinstance(paths, pathlib.Path):
            paths = str(paths)

        (base, pattern) = utils.split_path_by_marker(paths)

        if not pattern:
            yield pathlib.Path(base)
            return

        base_2 = pathlib.Path(base or '.').resolve()
        for path in sorted(base_2.glob(pattern)):
            yield path

    elif utils.is_io_stream(paths):
        yield paths  # type: ignore

    else:
        for path in paths:  # type: ignore
            for cpath in expand_paths_itr(path):
                yield cpath


def expand_paths(paths: PathOrPathsT) -> typing.List[IOInfo]:
    """
    :param paths:
        A glob path pattern string or pathlib.Path object holding such path, or
        a list consists of path strings or glob path pattern strings or
        pathlib.Path object holding such ones, or file objects
    """
    return [factory.make(p) for p in expand_paths_itr(paths)]

# vim:sw=4:ts=4:et:
