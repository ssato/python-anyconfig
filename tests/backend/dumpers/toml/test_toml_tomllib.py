#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for the dumper."""
from __future__ import annotations

import typing

import pytest

from ... import common

if typing.TYPE_CHECKING:
    import pathlib


try:
    DATA = common.load_data_for_testfile(__file__, load_idata=True)
except FileNotFoundError:
    pytest.skip(
        f"Not found test data for: {__file__}",
        allow_module_level=True
    )

NAMES: tuple[str, ...] = ("ipath", "idata", "opts", "exp")
DATA_IDS: list[str] = common.get_test_ids(DATA)
Parser = getattr(common.get_mod(__file__), "Parser", None)

if Parser is None:
    pytest.skip(
        f"Skip test cases: {__file__}",
        allow_module_level=True
    )


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_dumps(ipath: str, idata, opts: dict, exp: str) -> None:
    psr = Parser()
    content = psr.dumps(idata, **opts)

    assert psr.loads(content, **opts) == idata
    # assert content == exp  # This may fail.


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_dump(
    ipath: str, idata, opts: dict, exp: str, tmp_path: pathlib.Path
) -> None:
    psr = Parser()

    opath = tmp_path / f"{ipath.stem}.{psr.extensions()[0]}"
    ioi = common.ioinfo_from_path(opath)

    psr.dump(idata, ioi, **opts)

    assert opath.exists()
    assert psr.load(ioi, **opts) == idata

    # content = psr.ropen(str(opath)).read().decode("utf-8")
    # assert content == exp  # This may fail.
