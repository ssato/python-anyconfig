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


class TData(typing.NamedTuple):
    """A namedtuple object keeps test data.

    - datadir: A dir wheere data files exist
    - inp_path: A input file path
    - inp: An input data loaded from ``inp_path``
    - exp: Data gives an expected result
    - opts: Data gives options
    - scm: Data gives a path to schema file
    - query: A query string
    - ctx: Data gives a context object
    """
    datadir: pathlib.Path
    inp_path: pathlib.Path
    inp: InDataExT
    exp: DictT
    opts: DictT
    scm: typing.Union[pathlib.Path, str]
    query: str
    ctx: DictT

# vim:sw=4:ts=4:et:
