#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports
import unittest

import pytest

import anyconfig.backend.properties as TT
import tests.backend.common as TBC

from collections import OrderedDict


CNF = OrderedDict((("a", "0"), ("b", "bbb"), ("c", ""),
                   ("sect0.c", "x;y;z"), ("sect1.d", "1,2,3"),
                   ("d", "val1,val2,val3")))


class HasParserTrait(TBC.HasParserTrait):

    psr = TT.Parser()
    cnf = CNF
    cnf_s = TBC.read_from_res("20-00-cnf.properties")


@pytest.mark.parametrize(
    'inp,exp',
    (
     (' ', (None, '')),
     ('aaa', ('aaa', '')),
     ),
)
def test_parseline_warnings(inp, exp):
    with pytest.warns(SyntaxWarning):
        assert TT.parseline(inp) == exp


@pytest.mark.parametrize(
    'inp,exp',
    (
     ('aaa:', ('aaa', '')),
     (' aaa:', ('aaa', '')),
     ('url = http://localhost', ('url', 'http://localhost')),
     ('calendar.japanese.type: LocalGregorianCalendar',
      ('calendar.japanese.type', 'LocalGregorianCalendar')),
     ),
)
def test_parseline(inp, exp):
    assert TT.parseline(inp) == exp


class Test_00(unittest.TestCase):

    def test_10_unescape(self):
        exp = "aaa:bbb"
        res = TT.unescape(r"aaa\:bbb")
        self.assertEqual(res, exp, res)

    def test_12_unescape(self):
        exp = r"\a"
        res = TT.unescape(r"\\a")
        self.assertEqual(res, exp, res)

    def test_20_escape(self):
        exp = r"\:\=\\ "
        res = TT.escape(r":=\ ")
        self.assertEqual(res, exp, res)


class Test_10(TBC.Test_10_dumps_and_loads, HasParserTrait):

    load_options = dict(comment_markers=("//", "#", "!"))
    dump_options = dict(dummy_opt="this_will_be_ignored")


class Test_20(TBC.Test_20_dump_and_load, HasParserTrait):

    pass

# vim:sw=4:ts=4:et:
