#
# Copyright (C) 2017 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
from __future__ import absolute_import

import unittest
import anyconfig.query as TT

# from tests.common import dicts_equal


class Test_00_Functions(unittest.TestCase):

    def test_10_query(self):
        try:
            if TT.jmespath:
                self.assertEquals(TT.query({"a": 1}, ac_query="a"), 1)
                self.assertEquals(TT.query({"a": {"b": 2}}, ac_query="a.b"),
                                  2)
        except (NameError, AttributeError):
            pass

# vim:sw=4:ts=4:et:
