#
# Copyright (C) 2011 - 2016 Satoru SATOH <ssato at redhat.com>
#
# pylint: disable=missing-docstring
from __future__ import absolute_import
import unittest


def dicts_equal(lhs, rhs):
    """
    Check dicts' equality.
    """
    if len(lhs.keys()) != len(rhs.keys()):
        return False

    for key, val in rhs.items():
        val_ref = lhs.get(key, None)
        if val != val_ref:
            return False

    return True


class Test00(unittest.TestCase):

    def test_10_dicts_equal(self):
        self.assertTrue(dicts_equal({}, {}))
        self.assertFalse(dicts_equal({}, {'a': 1}))

        dic0 = {'a': 1}
        dic1 = {'a': [1, 2, 3]}
        self.assertTrue(dicts_equal(dic0, dic0))
        self.assertFalse(dicts_equal(dic0, dic1))

# vim:sw=4:ts=4:et:
