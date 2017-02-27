#
# Copyright (C) 2017 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
from __future__ import absolute_import

import unittest
import anyconfig.filter as TT

# from tests.common import dicts_equal


class Test_00_Functions(unittest.TestCase):

    def test_10_filter_(self):
        try:
            if TT.jmespath:
                self.assertEquals(TT.filter_({"a": 1}, ac_filter="a"), 1)
                self.assertEquals(TT.filter_({"a": {"b": 2}},
                                             ac_filter="a.b"),
                                  2)
        except NameError:
            pass

# vim:sw=4:ts=4:et:
