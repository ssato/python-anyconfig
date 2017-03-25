#
# Copyright (C) 2017 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
from __future__ import absolute_import

import os
import unittest
import anyconfig.query as TT

from tests.common import dicts_equal


class Test_00_Functions(unittest.TestCase):

    def _assert_dicts_equal(self, dic, ref):
        self.assertTrue(dicts_equal(dic, ref),
                        "%r%s vs.%s%r" % (dic, os.linesep, os.linesep, ref))

    def test_10_query(self):
        try:
            if TT.jmespath:
                self.assertEquals(TT.query({"a": 1}, ac_query="a"), 1)
                self.assertEquals(TT.query({"a": {"b": 2}}, ac_query="a.b"),
                                  2)
        except (NameError, AttributeError):
            pass

    def test_12_invalid_query(self):
        data = {"a": 1}
        try:
            if TT.jmespath:
                self._assert_dicts_equal(TT.query(data, ac_query="b."), data)
        except (NameError, AttributeError):
            pass

    def test_14_empty_query(self):
        data = {"a": 1}
        try:
            if TT.jmespath:
                self._assert_dicts_equal(TT.query(data, ac_query=None), data)
                self._assert_dicts_equal(TT.query(data, ac_query=''), data)
        except (NameError, AttributeError):
            pass

# vim:sw=4:ts=4:et:
