#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports
"""Test cases for the loader.
"""
from __future__ import annotations

import pathlib
import typing

import pytest

import tests.common.tdi_base
import tests.common.loader

from ... import common


try:
    DATA_0 = common.load_data_for_testfile(__file__)
except FileNotFoundError:
    pytest.skip(
        f"Not found test data for: {__file__}",
        allow_module_level=True
    )

DATA_IDS_0: list[str] = common.get_test_ids(DATA_0)
Parser = getattr(common.get_mod(__file__), "Parser", None)

assert Parser is not None


@pytest.mark.parametrize(common.NAMES, DATA_0, ids=DATA_IDS_0)
def test_loads(ipath: str, opts: dict, exp) -> None:
    psr = Parser()
    content = psr.ropen(ipath).read()

    assert psr.loads(content, **opts) == exp


@pytest.mark.parametrize(common.NAMES, DATA_0, ids=DATA_IDS_0)
def test_load(ipath: str, opts: dict, exp) -> None:
    psr = Parser()
    ioi = common.ioinfo_from_path(ipath)

    assert psr.load(ioi, **opts) == exp


class TDI(tests.common.tdi_base.TDI):
    _cid = tests.common.tdi_base.name_from_path(__file__)


(TT, DATA, DATA_IDS) = TDI().get_all()

if TT is None:
    pytest.skip(
        f"skipping tests: {TDI().cid()} as it's not available.",
        allow_module_level=True
    )

assert DATA


class TestCase(tests.common.loader.TestCase):
    psr_cls = TT.Parser

    @pytest.mark.parametrize(
        ("ipath", "aux"), DATA, ids=DATA_IDS,
    )
    def test_loads(
        self, ipath: pathlib.Path, aux: dict[str, typing.Any]
    ):
        self._assert_loads(ipath, aux)

    @pytest.mark.parametrize(
        ("ipath", "aux"), DATA, ids=DATA_IDS,
    )
    def test_load(
        self, ipath: pathlib.Path, aux: dict[str, typing.Any]
    ):
        self._assert_load(ipath, aux)
