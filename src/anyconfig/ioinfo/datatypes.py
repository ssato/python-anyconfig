#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=inherit-non-class,too-few-public-methods
"""anyconfig basic data types."""
import pathlib
import typing


IOI_PATH_OBJ: str = 'pathlib.Path'
IOI_STREAM: str = 'stream'


class IOInfo(typing.NamedTuple):
    """Equivalent to collections.namedtuple."""

    src: typing.Union[pathlib.Path, typing.IO]
    type: str
    path: str
    extension: str


IOI_KEYS: typing.Tuple[str, ...] = IOInfo._fields

PathOrIOT = typing.Union[str, pathlib.Path, typing.IO]
PathOrIOInfoT = typing.Union[PathOrIOT, IOInfo]

# vim:sw=4:ts=4:et:
