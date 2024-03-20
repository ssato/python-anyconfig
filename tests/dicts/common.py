#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
import unittest

from .. import base


class Collector(base.TDataCollector):
    ordered: bool = True


class TestCase(unittest.TestCase, Collector):

    def setUp(self):
        self.init()

# vim:sw=4:ts=4:et:
