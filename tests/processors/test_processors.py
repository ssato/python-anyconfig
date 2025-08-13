#
# Copyright (C) 2018 - 2025 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
import operator

import pytest

import anyconfig.processors.processors as TT

from .common import A, A2, B, C, PRS


def test_processort_compare() -> None:
    (a1, a2, a22, b) = (A(), A(), A2(), B())
    assert a1 == a2
    assert a1 != b
    assert a1 != a22


def test_processor_init():
    prcs = TT.Processors()
    assert not prcs.list()


def test_processor_init_with_processors():
    prcs = TT.Processors(PRS)
    assert prcs.list(sort=True) == sorted(
        PRS,
        key=operator.methodcaller("cid")
    )


def test_processor_list_by_cid():
    prcs = TT.Processors(PRS)
    exp = sorted(
        ((p.cid(), [p]) for p in PRS),
        key=TT.operator.itemgetter(0)
    )
    assert prcs.list_by_cid() == exp


def test_processor_list_x():
    prcs = TT.Processors(PRS)
    with pytest.raises(ValueError):
        prcs.list_x()

    assert prcs.list_x("cid") == sorted({p.cid() for p in PRS})
    assert prcs.list_x("type") == sorted({p.type() for p in PRS})

    res = sorted(set(A.extensions() + B.extensions() + C.extensions()))
    assert prcs.list_x("extension") == res
