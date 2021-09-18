#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name
r"""test cases for anyconfig.utils.lists.
"""
import operator
import unittest

import anyconfig.utils.lists as TT


class TestCase(unittest.TestCase):

    def test_groupby(self):
        items = (('a', 1), ('b', -1), ('c', 1))
        res = TT.groupby(items, operator.itemgetter(1))
        self.assertEqual(
            [(key, tuple(grp)) for key, grp in res],
            [(-1, (('b', -1),)), (1, (('a', 1), ('c', 1)))]
        )

    def test_concat(self):
        ies = (
            ([[]], []),
            ((()), []),
            ([[1, 2, 3], [4, 5]], [1, 2, 3, 4, 5]),
            ([[1, 2, 3], [4, 5, [6, 7]]], [1, 2, 3, 4, 5, [6, 7]]),
            (((1, 2, 3), (4, 5, (6, 7))), [1, 2, 3, 4, 5, (6, 7)]),
            (((i, i * 2) for i in range(3)), [0, 0, 1, 2, 2, 4]),
        )
        for inp, exp in ies:
            self.assertEqual(TT.concat(inp), exp)

# vim:sw=4:ts=4:et:
