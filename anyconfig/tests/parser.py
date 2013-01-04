#
# Copyright (C) 2011, 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.parser as P

import os
import os.path
import sys
import tempfile
import unittest


class Test_parser(unittest.TestCase):

    def test_00_parse_single(self):
        self.assertEquals(P.parse_single(""), "")
        self.assertEquals(P.parse_single("0"), 0)
        self.assertEquals(P.parse_single("123"), 123)
        self.assertEquals(P.parse_single("True"), True)
        self.assertEquals(P.parse_single("a string"), "a string")
        self.assertEquals(P.parse_single("0.1"), "0.1")
        self.assertEquals(
            P.parse_single("    a string contains extra whitespaces     "),
            "a string contains extra whitespaces"
        )

    def test_01_parse_list(self):
        self.assertEquals(P.parse_list(""), [])
        self.assertEquals(P.parse_list("a,b"), ["a", "b"])
        self.assertEquals(P.parse_list("1,2"), [1, 2])
        self.assertEquals(P.parse_list("a,b,"), ["a", "b"])
        self.assertEquals(P.parse_list("a|b|", "|"), ["a", "b"])

    def test_02_parse_attrlist_0(self):
        self.assertEquals(
            P.parse_attrlist_0("requires:bash,zsh"),
            [('requires', ['bash', 'zsh'])]
        )
        self.assertEquals(
            P.parse_attrlist_0("obsoletes:sysdata;conflicts:sysdata-old"),
            [('obsoletes', ['sysdata']), ('conflicts', ['sysdata-old'])]
        )

    def test_03_parse(self):
        pass


# vim:sw=4:ts=4:et:
