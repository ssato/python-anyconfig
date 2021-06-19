#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.api._load as TT

from ... import base


class Collector(base.TDataCollector):

    @staticmethod
    def target_fn(*args, **kwargs):
        return TT.single_load(*args, **kwargs)


class TestCase(unittest.TestCase, Collector):

    def setUp(self):
        self.init()

    def test_single_load(self):
        for data in self.each_data():
            self.assertEqual(
                self.target_fn(data.inp_path, **data.opts),
                data.exp,
                data
            )

    def test_single_load_intentional_failures(self):
        for data in self.each_data():
            with self.assertRaises(AssertionError):
                self.assertEqual(
                    self.target_fn(data.inp_path, **data.opts),
                    None
                )

# vim:sw=4:ts=4:et:
