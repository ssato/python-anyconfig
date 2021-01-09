#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""anyconfig type aliases.
"""
import pathlib
import typing


IterableT = typing.Iterable
ListT = typing.List

ConfigT = typing.Mapping
SchemaT = typing.Mapping

PathT = typing.Union[str, pathlib.Path]
FileOrPathT = typing.Union[PathT, typing.IO]
FileOrPathOrIOInfoT = typing.Union[FileOrPathT, typing.NamedTuple]

ContextT = typing.Mapping

MaybeDataT = typing.Optional[typing.Mapping]

ParserTypeT = str

# vim:sw=4:ts=4:et:
