#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import
import unittest
import anyconfig.backend.properties as TT
import anyconfig.backend.tests.ini

from anyconfig.compat import OrderedDict as ODict


CNF_S = """
a = 0
  b = bbb
c:

sect0.c = x;y;z
sect1.d = \\
    1,2,3
"""
CNF = ODict((("a", "0"), ("b", "bbb"), ("c", ""),
             ("sect0.c", "x;y;z"), ("sect1.d", "1,2,3")))


class Test00(unittest.TestCase):

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


class Test10(anyconfig.backend.tests.ini.Test10):

    cnf = CNF
    cnf_s = CNF_S
    load_options = dict(comment_markers=("//", "#", "!"))
    dump_options = dict(dummy_opt="this_will_be_ignored")

    def setUp(self):
        self.psr = TT.Parser()


class Test20(anyconfig.backend.tests.ini.Test20):

    psr_cls = TT.Parser
    cnf = CNF
    cnf_s = CNF_S
    cnf_fn = "conf.properties"

# vim:sw=4:ts=4:et:
