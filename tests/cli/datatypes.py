#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"""Basic data types for file based test data collectors.
"""
from __future__ import annotations

import pathlib
import typing


DictT = dict[str, typing.Any]


class Expected(typing.NamedTuple):
    """Keeps expected result's info.
    """
    exit_code: int = 0
    exit_code_matches: bool = True
    words_in_stdout: str = ''
    words_in_stderr: str = ''
    exception: BaseException = SystemExit


class TData(typing.NamedTuple):
    """A namedtuple object keeps test data to test cases with no file outputs.
    """
    datadir: pathlib.Path
    inp_path: pathlib.Path
    opts: list[str] = []
    exp: Expected = Expected()

    # Optional extra data.
    outname: str = ''
    ref: typing.Optional[DictT] = None
    oo_opts: DictT = {}
    scm: typing.Optional[pathlib.Path] = None


class TDataSet(typing.NamedTuple):
    """A namedtuple object keeps test data to test cases with no file outputs.
    """
    datadir: pathlib.Path
    inputs: list[pathlib.Path]
    opts: list[str] = []
    exp: Expected = Expected()

    # Likewise.
    outname: str = ''
    ref: typing.Optional[DictT] = None
    oo_opts: DictT = {}
    scm: typing.Optional[pathlib.Path] = None
