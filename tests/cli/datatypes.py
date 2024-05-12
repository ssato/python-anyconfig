#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"""Basic data types for file based test data loaders."""
from __future__ import annotations

import pathlib
import typing


DictType = dict[str, typing.Any]


class Expected(typing.NamedTuple):
    """Keeps expected result's information."""
    exit_code: int = 0
    exit_code_matches: bool = True
    words_in_stdout: str = ""
    words_in_stderr: str = ""
    exception: BaseException = SystemExit


class TData(typing.NamedTuple):
    """A namedtuple object keeps test data for test cases with no file outputs.
    """
    ipath: pathlib.Path
    ipaths: list[str] = []
    opts: list[str] = []
    exp: Expected = Expected()

    # Optional extra data.
    outname: str = ""
    ref: typing.Optional[DictType] = None
    oo_opts: DictType = {}
    scm: typing.Optional[pathlib.Path] = None


class TDataSet(typing.NamedTuple):
    """A namedtuple object keeps test data to test cases with no file outputs.
    """
    datadir: pathlib.Path
    inputs: list[pathlib.Path]
    opts: list[str] = []
    exp: Expected = Expected()

    # Likewise.
    outname: str = ""
    ref: typing.Optional[DictType] = None
    oo_opts: DictType = {}
    scm: typing.Optional[pathlib.Path] = None
