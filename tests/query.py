#
# Copyright (C) 2017 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
from __future__ import absolute_import

import os
import unittest
import anyconfig.query as TT


class Test_00_Functions(unittest.TestCase):

    def _assert_dicts_equal(self, dic, ref):
        self.assertEqual(dic, ref,
                         "%r%s vs.%s%r" % (dic, os.linesep, os.linesep, ref))

    def _assert_query(self, data_exp_ref_list, dicts=False):
        _assert = self._assert_dicts_equal if dicts else self.assertEqual
        for data, exp, ref in data_exp_ref_list:
            try:
                _assert(TT.query(data, exp)[0], ref)
            except ValueError:
                pass

    def test_10_query(self):
        self._assert_query([({"a": 1}, "a", 1),
                            ({"a": {"b": 2}}, "a.b", 2)])

    def test_12_invalid_query(self):
        data = {"a": 1}
        self._assert_query([(data, "b.", data)])

    def test_14_empty_query(self):
        data = {"a": 1}
        self._assert_query([(data, None, data),
                            (data, '', data)])

# vim:sw=4:ts=4:et:
