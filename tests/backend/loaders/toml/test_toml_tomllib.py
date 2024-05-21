#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for the loader."""
from __future__ import annotations

import pytest

from ... import common


try:
    DATA = common.load_data_for_testfile(__file__)
except FileNotFoundError:
    pytest.skip(
        f"Not found test data for: {__file__}",
        allow_module_level=True
    )

DATA_IDS: list[str] = common.get_test_ids(DATA)
Parser = getattr(common.get_mod(__file__), "Parser", None)

if Parser is None:
    pytest.skip(
        f"Skip test cases: {__file__}",
        allow_module_level=True
    )


@pytest.mark.parametrize(common.NAMES, DATA, ids=DATA_IDS)
def test_loads(ipath: str, opts: dict, exp) -> None:
    psr = Parser()
    content = psr.ropen(ipath).read().decode("utf-8")

    assert psr.loads(content, **opts) == exp


@pytest.mark.parametrize(common.NAMES, DATA, ids=DATA_IDS)
def test_load(ipath: str, opts: dict, exp) -> None:
    psr = Parser()
    ioi = common.ioinfo_from_path(ipath)

    assert psr.load(ioi, **opts) == exp
