#
# Copyright (C) 2018 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name
import operator
import unittest

import anyconfig.processors.processors as TT

from .common import A, A2, B, C, PRS


class Test_10_Processor(unittest.TestCase):

    def test_10_eq(self):
        (a1, a2, a22, b) = (A(), A(), A2(), B())
        self.assertEqual(a1, a2)
        self.assertNotEqual(a1, b)
        self.assertNotEqual(a1, a22)


class Test_40_Processors(unittest.TestCase):

    def test_10_init(self):
        prcs = TT.Processors()
        self.assertFalse(prcs.list())

    def test_12_init_with_processors(self):
        prcs = TT.Processors(PRS)
        self.assertEqual(prcs.list(sort=True),
                         sorted(PRS, key=operator.methodcaller('cid')))

    def test_20_list_by_cid(self):
        prcs = TT.Processors(PRS)
        exp = sorted(((p.cid(), [p]) for p in PRS),
                     key=TT.operator.itemgetter(0))
        self.assertEqual(prcs.list_by_cid(), exp)

    def test_20_list_x(self):
        prcs = TT.Processors(PRS)
        self.assertRaises(ValueError, prcs.list_x)
        self.assertEqual(prcs.list_x('cid'),
                         sorted(set(p.cid() for p in PRS)))
        self.assertEqual(prcs.list_x('type'),
                         sorted(set(p.type() for p in PRS)))

        res = sorted(set(A.extensions() + B.extensions() + C.extensions()))
        self.assertEqual(prcs.list_x('extension'), res)

# vim:sw=4:ts=4:et:
