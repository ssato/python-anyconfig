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

import anyconfig.backend.json.default as TT
import tests.common.tdi_base


class TDI(tests.common.tdi_base.TDI):
    _cid = tests.common.tdi_base.name_from_path(__file__)


DATA_AND_IDS_0 = TDI().gets()


class TestCase(tests.common.tdi_base.Base):
    psr_cls = getattr(TT, "Parser")

    @pytest.mark.parametrize(
        ("ipath", "aux"),
        DATA_AND_IDS_0[0],
        ids=DATA_AND_IDS_0[1],
    )
    def test_loads_and_load(
        self, ipath: pathlib.Path, aux: typing.Dict[str, typing.Any],
        debug: bool = False,
    ):
        self.assert_loads_and_load_impl(ipath, aux, debug)
