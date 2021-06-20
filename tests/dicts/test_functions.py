#
# Forked from m9dicts.tests.{api,dicts}
#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
#
# pylint: disable=missing-docstring,invalid-name
import collections
import unittest

import anyconfig.dicts as TT


class TestCase(unittest.TestCase):

    # FIXME: Add some more test cases
    def test_set_(self):
        aes = (
            ((dict(a=1, b=dict(c=2, )), 'a.b.d', 3),
             dict(a=dict(b=dict(d=3)), b=dict(c=2))),
        )
        for args, exp in aes:
            TT.set_(*args)
            self.assertEqual(args[0], exp)

    # FIXME: Add some more test cases
    def test_convert_to(self):
        OD = collections.OrderedDict
        aes = (
            ((OD((('a', 1), )), False, dict), dict(a=1)),
            ((OD((('a', OD((('b', OD((('c', 1), ))), ))), )), False, dict),
             dict(a=dict(b=dict(c=1)))),
        )
        for args, exp in aes:
            self.assertEqual(TT.convert_to(*args), exp)

# vim:sw=4:ts=4:et:
