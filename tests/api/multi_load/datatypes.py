#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Common data types for api.multi_load test cases.
"""
import pathlib
import typing


DictT = typing.Dict[str, typing.Any]


class TData(typing.NamedTuple):
    """A namedtuple object keeps test data.
    """
    datadir: pathlib.Path
    inputs: typing.List[pathlib.Path]  # Same as the above.
    exp: DictT
    opts: DictT
    scm: pathlib.Path
    query: str
    ctx: DictT

# vim:sw=4:ts=4:et:
