#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

from ... import base


class TestCase(unittest.TestCase, base.TDataCollector):
    pattern = '*.txt'

    def setUp(self):
        self.init()

# vim:sw=4:ts=4:et:
