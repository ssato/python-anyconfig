#
# Copyright (C) 2016 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports,protected-access
"""Test cases for .backend.shellvars."""
import collections
import io

import pytest

import anyconfig.backend.shellvars as TT
import tests.backend.common as TBC


CNF = collections.OrderedDict(
    (('a', '0'), ('b', 'bbb'), ('c', 'ccc'), ('d', 'ddd'), ('e', 'eee'))
)


@pytest.mark.parametrize(
    'inp,exp',
    (
     ('aaa=', ('aaa', '')),
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
    (
     ('', {}),
     ('# ', {}),
     ('aaa=', {'aaa': ''}),
     ('aaa=bbb', {'aaa': 'bbb'}),
     ('aaa=bbb # ...',  {'aaa': 'bbb'}),
     ),
)
def test_load(inp, exp):
    assert TT.load(io.StringIO(inp)) == exp


class HasParserTrait(TBC.HasParserTrait):

    psr = TT.Parser()
    cnf = CNF
    cnf_s = TBC.read_from_res('20-00-cnf.sh')


class Test_10(TBC.Test_10_dumps_and_loads, HasParserTrait):

    pass


class Test_20(TBC.Test_20_dump_and_load, HasParserTrait):

    pass

# vim:sw=4:ts=4:et:
