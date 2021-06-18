#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.query

from . import common


@unittest.skipIf(not anyconfig.query.SUPPORTED,
                 'jmespath lib is not available')
class TestCase(common.TestCase):
    kind = 'query'

    def test_single_load(self):
        for data in self.each_data():
            self.assertEqual(
                self.target_fn(
                    data.inp_path, ac_query=data.query.strip(), **data.opts
                ),
                data.exp,
                f'{data.datadir!s}, {data.inp_path!s}'
            )

    def test_single_load_with_invalid_query_string(self):
        for data in self.each_data():
            self.assertEqual(
                self.target_fn(
                    data.inp_path, ac_query=None, **data.opts
                ),
                self.target_fn(data.inp_path, **data.opts),
                f'{data.datadir!s}, {data.inp_path!s}'
            )

    def test_single_load_intentional_failures(self):
        for data in self.each_data():
            with self.assertRaises(AssertionError):
                exp = dict(z=1, zz='zz', zzz=[1, 2, 3], zzzz=dict(z=0))
                self.assertEqual(
                    self.target_fn(
                        data.inp_path, ac_query=data.query, **data.opts
                    ),
                    exp
                )

# vim:sw=4:ts=4:et:
