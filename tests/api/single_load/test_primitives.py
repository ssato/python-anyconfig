#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import anyconfig.api._load as TT

from . import common


class TestCase(common.BaseTestCase):
    kind = 'primitives'

    def test_single_load(self):
        for data in self.each_data():
            self.assertEqual(
                TT.single_load(data.inp_path, **data.opts),
                data.exp,
                f'{data.datadir!s}, {data.inp_path!s}'
            )

    def test_single_load_intentional_failures(self):
        for data in self.each_data():
            with self.assertRaises(AssertionError):
                self.assertEqual(
                    TT.single_load(data.inp_path, **data.opts),
                    None
                )

# vim:sw=4:ts=4:et:
