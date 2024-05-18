#
# Copyright (C) 2013 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, too-many-arguments
"""Test cases of anyconfig.cli.main with ignore-missing option."""
from __future__ import annotations

import typing

import pytest

from .. import common
from . import datatypes
from .common import run_main, NAMES_WITH_REF as NAMES

if typing.TYPE_CHECKING:
    import pathlib


DATA = common.load_data_for_testfile(
    __file__, values=(("o", []), ("e", None), ("on", ""), ("r", None)),
)
DATA_IDS: list[str] = common.get_test_ids(DATA)


def test_data():
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_cli(
    ipath: pathlib.Path, opts: list[str], exp: dict, oname: str, ref,
    tmp_path: pathlib.Path
) -> None:
    expected = datatypes.Expected(**exp)
    tdata = datatypes.TData(
        ipath, [str(ipath), "file_not_exist.json"], opts, expected, oname, ref
    )
    run_main(tdata, tmp_path)
