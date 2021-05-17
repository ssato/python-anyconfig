#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""test cases for anyconfig.utils.lists.
"""
import unittest

import anyconfig.utils.utils as TT


class TestCase(unittest.TestCase):

    def test_filter_options(self):
        data = (
            (('aaa', ), dict(aaa=1, bbb=2), dict(aaa=1)),
            (('aaa', ), dict(bbb=2), dict()),
        )
        for keys, inp, exp in data:
            self.assertEqual(TT.filter_options(keys, inp), exp)

# vim:sw=4:ts=4:et:
