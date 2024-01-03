#
# Copyright (C) 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name
r"""Test cases for tests.common.tdi.
"""
from . import tdi as TT


class StdJsonLoaderTDI(TT.TDI):
    _cid: str = "std.json"


class StdJsonOrderedLoaderTDI(StdJsonLoaderTDI):
    keep_order = True


def test_StdJsonLoaderTDI():
    tdi = StdJsonLoaderTDI()
    assert tdi.cid() == StdJsonLoaderTDI.cid()

    tdi.load()
    assert tdi.get()


def test_StdJsonOrderdLoaderTDI():
    tdi = StdJsonOrderedLoaderTDI()
    assert tdi.cid() == StdJsonOrderedLoaderTDI.cid()

    tdi.load()
    assert tdi.get()
