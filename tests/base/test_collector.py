#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=invalid-name,missing-docstring
import unittest
import pathlib

from . import collector as TT


CUR_DIR = pathlib.Path(__file__).parent


class Collector(TT.TDataCollector):
    # To avoid error because there are no files with '.json' file extension in
    # tests/res/base/basics/20/.
    pattern = '*.*'
    should_exist = ()  # Likewise.


class TestCase(unittest.TestCase, Collector):

    def setUp(self):
        self.init()

    def test_members(self):
        self.assertTrue(self.target)
        self.assertNotEqual(self.target, TT.TDataCollector.target)
        self.assertEqual(self.target, CUR_DIR.name)

        self.assertTrue(self.root is not None)
        self.assertEqual(
            self.root,
            CUR_DIR.parent / 'res' / self.target / self.kind
        )

        self.assertTrue(self.datasets)

# vim:sw=4:ts=4:et:
