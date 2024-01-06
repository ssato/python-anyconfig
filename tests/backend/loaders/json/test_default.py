#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports
"""Test cases for the loader, std.json.
"""
import pathlib
import typing

import anyconfig.backend.json.default as TT
import anyconfig.ioinfo
import tests.common.tdi

import pytest


class TDI(tests.common.tdi.TDI):
    _cid = "std.json"


TDI0 = TDI()
TDI0.load()

DATA0 = TDI0.get()


@pytest.mark.parametrize(
    ("ipath", "aux"),
    DATA0,
    ids=[i.name for i, _aux in DATA0],
)
def test_loads(
    ipath: pathlib.Path, aux: typing.Dict[str, typing.Any]
):
    exp = aux["e"]  # It may fail.
    opt = aux.get("o", {})
    ioi = anyconfig.ioinfo.make(ipath)

    psr = TT.Parser()
    assert psr.loads(ipath.read_text(), **opt) == exp
    assert psr.load(ioi, **opt) == exp
