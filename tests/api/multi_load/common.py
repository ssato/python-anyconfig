#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Common utility functions.
"""
import unittest

import anyconfig.api._load as TT

from . import collector


class TestCase(unittest.TestCase, collector.DataCollector):

    @staticmethod
    def target_fn(*args, **kwargs):
        return TT.multi_load(*args, **kwargs)

    def setUp(self):
        self.init()

    def test_multi_load(self):
        for tdata in self.each_data():
            self.assertEqual(
                self.target_fn(tdata.inputs, **tdata.opts),
                tdata.exp,
                tdata
            )

    def test_multi_load_failures(self):
        for tdata in self.each_data():
            with self.assertRaises(AssertionError):
                self.assertEqual(
                    self.target_fn(tdata.inputs, **tdata.opts),
                    None,
                    tdata
                )

# vim:sw=4:ts=4:et:
