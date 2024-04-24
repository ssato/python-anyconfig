#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""test cases for anyconfig.utils.lists."""
from __future__ import annotations

import operator

import pytest

import anyconfig.utils.lists as TT


def test_groupby() -> None:
    items = (("a", 1), ("b", -1), ("c", 1))
    res = TT.groupby(items, operator.itemgetter(1))
    assert [
        (key, tuple(grp)) for key, grp in res
    ] == [(-1, (("b", -1),)), (1, (("a", 1), ("c", 1)))]


@pytest.mark.parametrize(
    ("xss", "exp"),
    (([[]], []),
     ((()), []),
     ([[1, 2, 3], [4, 5]], [1, 2, 3, 4, 5]),
     ([[1, 2, 3], [4, 5, [6, 7]]], [1, 2, 3, 4, 5, [6, 7]]),
     (((1, 2, 3), (4, 5, (6, 7))), [1, 2, 3, 4, 5, (6, 7)]),
     (((i, i * 2) for i in range(3)), [0, 0, 1, 2, 2, 4])
     ),
)
def test_concat(xss, exp):
    assert TT.concat(xss) == exp
