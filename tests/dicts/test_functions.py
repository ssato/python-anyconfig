#
# Copyright (C) 2021 - 2025 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,protected-access
"""Test cases for some functions in anyconfig.parser."""
from __future__ import annotations

import collections

import pytest

import anyconfig.dicts as TT


@pytest.mark.parametrize(
    ("inp", "exp"),
    (("/a~1b", "/a/b"),
     ("~1aaa~1~0bbb", "/aaa/~bbb"),
     ),
)
def test_jsnp_unescape(inp, exp):
    assert TT._jsnp_unescape(inp) == exp


@pytest.mark.parametrize(
    ("args", "exp"),
    ((("", ), []),
     (("/", ), [""]),
     (("/a", ), ["a"]),
     ((".a", ), ["a"]),
     (("a", ), ["a"]),
     (("a.", ), ["a"]),
     (("/a/b/c", ), ["a", "b", "c"]),
     (("a.b.c", ), ["a", "b", "c"]),
     (("abc", ), ["abc"]),
     (("/a/b/c", ), ["a", "b", "c"]),
     ),
)
def test_split_path(args, exp):
    assert TT._split_path(*args) == exp


# FIXME: Add some more test cases
@pytest.mark.parametrize(
    ("args", "exp"),
    ((({"a": 1, "b": {"c": 2}}, "a.b.d", 3),
      {"a": {"b": {"d": 3}}, "b": {"c": 2}}),
     ),
)
def test_set_(args, exp):
    TT.set_(*args)
    assert args[0] == exp


OD = collections.OrderedDict


# FIXME: Likewise.
@pytest.mark.parametrize(
    ("obj", "opts", "exp"),
    ((OD((("a", 1), )),
      {"ac_ordered": False, "ac_dict": dict},
      {"a": 1}),
     (OD((("a", OD((("b", OD((("c", 1), ))), ))), )),
      {"ac_ordered": False, "ac_dict": dict},
      {"a": {"b": {"c": 1}}}),
     ),
)
def test_convert_to(obj, opts, exp):
    assert TT.convert_to(obj, **opts) == exp


@pytest.mark.parametrize(
    ("objs", "exp"),
    ((([], (), list(range(10)), list(range(4))), True),
     (([], {}), False),
     (([], "aaa"), False),
     ),
)
def test_are_list_like(objs, exp):
    assert TT._are_list_like(*objs) == exp
