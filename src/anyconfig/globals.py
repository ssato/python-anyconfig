#
# Copyright (C) 2013 - 2018 Satoru SATOH <ssato @ redhat.com>
# Copyright (C) 2019 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""anyconfig globals.
"""
import typing

from anyconfig.types import (
    FileOrPathT, ListT, ParserTypeT
)


IOI_KEYS: ListT = "src type path extension".split()
IOI_TYPES = (IOI_NONE, IOI_PATH_STR, IOI_PATH_OBJ, IOI_STREAM) = \
    (None, "path", "pathlib.Path", "stream")


class IOInfo(typing.NamedTuple):
    """Equivalent to collections.namedtuple."""
    src: FileOrPathT
    type: str
    path: str
    extension: str


class BaseError(RuntimeError):
    """Base Error exception."""

    _msg_fmt: str = 'forced_type: {!s}'

    def __init__(self, forced_type: typing.Optional[ParserTypeT]):
        super().__init__(self._msg_fmt.format(forced_type))


class UnknownParserTypeError(BaseError):
    """Raise if no parsers were found for given type."""
    _msg_fmt: str = 'No parser found for type: {!s}'


class UnknownProcessorTypeError(UnknownParserTypeError):
    """Raise if no processors were found for given type."""


class UnknownFileTypeError(BaseError):
    """Raise if not parsers were found for given file path."""
    _msg_fmt: str = 'No parser found for file: {!s}'

    def __init__(self, path: FileOrPathT):
        super().__init__(self._msg_fmt.format(path))

# vim:sw=4:ts=4:et:
