#
# Copyright (C) 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name
r"""Test cases for tests.common.tdi.
"""
import typing

import pytest

import tests.common.tdi_base
from . import tdi_base as TT


@pytest.mark.parametrize(
    ("path", "exp", "exc"),
    (("/0/1/2/a/b/c/test_foo_bar.py", "foo.bar", None),
     ("/0/1/2/foo.py", None, NameError),
     ),
)
def test_name_from_path(
    path: str, exp: str, exc: typing.Optional[Exception]
):
    if exc is None:
        assert TT.name_from_path(path) == exp
    else:
        with pytest.raises(exc):
            TT.name_from_path(path)


def test_tdi_base_original():
    tdi = TT.TDI()
    assert tdi.cid() == TT.TDI.cid()


class TDI(TT.TDI):
    _cid: str = tests.common.tdi_base.name_from_path(__file__)


def test_tdi_base():
    tdi = TDI()
    assert tdi.cid() == "tdi.base"


class FakeStdJsonLoaderTDI(TT.TDI):
    _cid: str = "std.json"  # override.


def test_tdi_base_children():
    tdi = FakeStdJsonLoaderTDI()
    assert tdi.cid() == FakeStdJsonLoaderTDI.cid()

    tdi.load()
    assert tdi.get()
