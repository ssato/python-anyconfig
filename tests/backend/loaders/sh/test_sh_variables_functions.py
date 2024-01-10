#
# Copyright (C) 2016 - 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports,protected-access
"""Test cases for .backend.sh.functions.*."""
import collections
import io

import pytest

import anyconfig.backend.sh.variables as TT


CNF = collections.OrderedDict(
    (('a', '0'), ('b', 'bbb'), ('c', 'ccc'), ('d', 'ddd'), ('e', 'eee'))
)


@pytest.mark.parametrize(
    'inp,exp',
    (('aaa=', ('aaa', '')),
     ('aaa=bbb', ('aaa', 'bbb')),
     ('aaa="bb b"', ('aaa', 'bb b')),
     # (r"aaa=bb\"b", ('aaa', 'bb"b')),  # todo?
     ('aaa=bbb   # ccc', ('aaa', 'bbb')),
     ),
)
def test_parseline(inp, exp):
    assert TT._parseline(inp) == exp


@pytest.mark.parametrize(
    'inp,exp',
    (('', {}),
     ('# ', {}),
     ('aaa=', {'aaa': ''}),
     ('aaa=bbb', {'aaa': 'bbb'}),
     ('aaa=bbb # ...', {'aaa': 'bbb'}),
     ),
)
def test_load(inp, exp):
    assert TT.load(io.StringIO(inp)) == exp
