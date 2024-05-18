#
# Copyright (C) 2013 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, too-many-arguments
"""Test cases of anyconfig.cli.main without arguments to show info."""
from __future__ import annotations

import typing

import pytest

import anyconfig.schema

from .. import common
from . import datatypes
from .common import run_main, NAMES

if typing.TYPE_CHECKING:
    import pathlib

if not anyconfig.schema.SUPPORTED:
    pytest.skip(
        "Library for JSON schema validation is not available",
        allow_module_level=True
    )


DATA = common.load_data_for_testfile(
    __file__, values=(("o", []), ("e", {}))
)
DATA_IDS: list[str] = common.get_test_ids(DATA)


def test_data():
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_cli(
    ipath: pathlib.Path, opts: list[str], exp: dict, tmp_path
) -> None:
    expected = datatypes.Expected(**exp)
    tdata = datatypes.TData(ipath, [], opts, expected)
    run_main(tdata, tmp_path)
