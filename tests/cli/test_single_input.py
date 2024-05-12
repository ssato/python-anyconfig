#
# Copyright (C) 2013 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, too-many-arguments
"""Test cases of anyconfig.cli.main with sinngle file innput."""
from __future__ import annotations

import typing

import pytest

import anyconfig.schema

from .. import common
from . import datatypes
from .common import run_main, NAMES_WITH_REF

if typing.TYPE_CHECKING:
    import pathlib

if not anyconfig.schema.SUPPORTED:
    pytest.skip(
        "Library for JSON schema validation is not available",
        allow_module_level=True
    )


NAMES: list[str] = (*NAMES_WITH_REF, "oopts")
DATA = common.load_data_for_testfile(
    __file__,
    values=(("o", []), ("e", {}), ("on", ""), ("r", {}), ("oo", {}))
)
DATA_IDS: list[str] = common.get_test_ids(DATA)


def test_data():
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_cli(
    ipath: pathlib.Path, opts: list[str], exp: dict,
    oname: str, ref: dict, oopts: dict,
    tmp_path: pathlib.Path
) -> None:
    expected = datatypes.Expected(**exp)
    tdata = datatypes.TData(
        ipath, [str(ipath)], opts, expected,
        outname=oname, ref=ref, oo_opts=oopts
    )
    run_main(tdata, tmp_path)
