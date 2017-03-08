#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# Copyright (C) 2017 Red Hat, Inc.
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports
from __future__ import absolute_import

import unittest
import anyconfig.backend.properties as TT
import tests.backend.common as TBC

from anyconfig.compat import OrderedDict


CNF_S = """
a = 0
  b = bbb
c:

sect0.c = x;y;z
sect1.d = \\
    1,2,3

d=\\
val1,\\
val2,\\
val3
"""
CNF = OrderedDict((("a", "0"), ("b", "bbb"), ("c", ""),
                   ("sect0.c", "x;y;z"), ("sect1.d", "1,2,3"),
                   ("d", "val1,val2,val3")))


class HasParserTrait(TBC.HasParserTrait):

    psr = TT.Parser()
    cnf = CNF
    cnf_s = CNF_S


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
