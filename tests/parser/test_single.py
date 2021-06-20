#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.parser.parse_single.
"""
import anyconfig.parser as TT

from . import common


class TestCase(common.TestCase):
    kind = 'single'
    pattern = '*.*'

    def test_parse_single(self):
        for data in self.each_data():
            self.assertEqual(TT.parse_single(data.inp), data.exp)

# vim:sw=4:ts=4:et:
