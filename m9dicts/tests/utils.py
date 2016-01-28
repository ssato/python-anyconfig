#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato @ redhat.com>
#
# pylint: disable=missing-docstring,invalid-name
from __future__ import absolute_import
import unittest
import m9dicts.utils as TT
from m9dicts.compat import OrderedDict


class Test_00_Functions(unittest.TestCase):

    def test_10_is_dict_like(self):
        self.assertFalse(TT.is_dict_like("a string"))
        self.assertTrue(TT.is_dict_like({}))
        self.assertTrue(TT.is_dict_like(OrderedDict((('a', 1), ('b', 2)))))

# vim:sw=4:ts=4:et:
