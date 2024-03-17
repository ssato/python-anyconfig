#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name
"""test cases for anyconfig.utils."""
import collections

import pytest

import anyconfig.utils.detectors as TT


@pytest.mark.parametrize(
    ("inp", "exp"),
    ((None, False),
     ([], True), ((), True),
     ((str(x) for x in range(10)), True),
     ([str(x) for x in range(10)], True),
     ("abc", False), (0, False), ({}, False),
     ),
)
def test_is_iterable(inp, exp):
    assert TT.is_iterable(inp) == exp


@pytest.mark.parametrize(
    ("inp", "exp"),
    ((None, False),
     (0, False),
     ("aaa", False),
     ({}, False),
     ([], True), ((), True),
     ((str(x) for x in range(10)), True),
     ([str(x) for x in range(10)], True),
     ),
)
def test_is_list_like(inp, exp):
    assert TT.is_list_like(inp) == exp


@pytest.mark.parametrize(
    ("inp", "exp"),
    ((None, False),
     (0, False),
     ("aaa", False),
     ([], False),
     ((1, ), False),
     (collections.namedtuple("Point", ("x", "y"))(1, 2), False),
     ({}, True),
     (collections.OrderedDict((("a", 1), ("b", 2))), True),
     ),
)
def test_is_dict_like(inp, exp):
    assert TT.is_dict_like(inp) == exp

# vim:sw=4:ts=4:et:
