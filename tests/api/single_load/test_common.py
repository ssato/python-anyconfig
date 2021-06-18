#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=invalid-name,missing-docstring
import unittest
import pathlib

from . import common
from ... import base


CUR_DIR = pathlib.Path(__file__).parent


class TestCase(common.TestCase):

    def test_members(self):
        self.assertNotEqual(self.target, base.TDataCollector.target)
        self.assertEqual(self.target, CUR_DIR.name)
        self.assertEqual(
            self.root,
            CUR_DIR.parent.parent / 'res' / self.target / self.kind
        )
        self.assertTrue(self.datasets)

    @unittest.skip("I have no idea how to implement this.")
    def test_target_fn(self):
        self.assertEqual(  # This is not satisfied clearly.
            self.target_fn, common.TT.single_load
        )

# vim:sw=4:ts=4:et:
