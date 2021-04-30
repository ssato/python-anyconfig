#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=inherit-non-class,too-few-public-methods
"""anyconfig basic data types.
"""
import pathlib
import typing


IOI_NONE = None
IOI_PATH_STR: str = 'path'
IOI_PATH_OBJ: str = 'pathlib.Path'
IOI_STREAM: str = 'stream'

IOI_TYPES: typing.FrozenSet[typing.Optional[str]] = frozenset(
    (IOI_NONE, IOI_PATH_STR, IOI_PATH_OBJ, IOI_STREAM)
)


class IOInfo(typing.NamedTuple):
    """Equivalent to collections.namedtuple."""
    src: typing.Optional[typing.Union[str, pathlib.Path, typing.IO]]
    type: str
    path: str
    extension: str


IOI_KEYS: typing.Tuple[str, ...] = IOInfo._fields

# vim:sw=4:ts=4:et:
