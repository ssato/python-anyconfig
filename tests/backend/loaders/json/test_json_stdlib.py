#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports
"""Test cases for the loader.
"""
import pathlib
import typing

import pytest

import tests.common.tdi_base
import tests.common.loader


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
    def test_loads_and_load(
        self, ipath: pathlib.Path, aux: typing.Dict[str, typing.Any],
        debug: bool = False,
    ):
        self.assert_loads_and_load_impl(ipath, aux, debug)
