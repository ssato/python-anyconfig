#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
"""File based test data collector.
"""
import pathlib
import typing

from anyconfig.api import InDataExT


DictT = typing.Dict[str, typing.Any]
MaybePathT = typing.Optional[pathlib.Path]


class TDataPaths(typing.NamedTuple):
    """A namedtuple object keeps test data paths."""
    datadir: pathlib.Path
    inp: pathlib.Path
    exp: MaybePathT
    opts: MaybePathT
    scm: MaybePathT
    query: MaybePathT
    ctx: MaybePathT


class TData(typing.NamedTuple):
    """A namedtuple object keeps test data.
    """
    datadir: pathlib.Path
    inp_path: pathlib.Path
    inp: InDataExT
    exp: DictT
    opts: DictT
    scm: typing.Union[pathlib.Path, str]
    query: typing.Union[pathlib.Path, str]
    ctx: DictT

# vim:sw=4:ts=4:et:
