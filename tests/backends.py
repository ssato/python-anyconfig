#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import unittest
import anyconfig.backends as TT

from anyconfig.globals import UnknownParserTypeError, UnknownFileTypeError


class Test(unittest.TestCase):

    def test_10_list_types(self):
        types = TT.list_types()

        self.assertTrue(isinstance(types, list))
        self.assertTrue(bool(list))  # ensure it's not empty.

    def test_20_find_parser_by_type__ng_cases(self):
        self.assertRaises(ValueError, TT.find_parser_by_type, None)
        self.assertRaises(UnknownParserTypeError, TT.find_parser_by_type,
                          "_unkonw_type_")

    def test_30_find_parser_ng_cases(self):
        self.assertRaises(ValueError, TT.find_parser, None)
        self.assertRaises(UnknownParserTypeError, TT.find_parser, None,
                          "_unkonw_type_")
        self.assertRaises(UnknownFileTypeError, TT.find_parser,
                          "cnf.unknown_ext")

# vim:sw=4:ts=4:et:
