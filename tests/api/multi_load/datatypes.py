#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"""Common data types for api.multi_load test cases.
"""
from __future__ import annotations

import pathlib
import typing


DictT = dict[str, typing.Any]


class TData(typing.NamedTuple):
    """A namedtuple object keeps test data.
    """
    datadir: pathlib.Path
    inputs: list[pathlib.Path]  # Same as the above.
    exp: DictT
    opts: DictT
    scm: pathlib.Path
    query: str
    ctx: DictT
