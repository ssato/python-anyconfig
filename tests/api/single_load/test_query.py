#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.api._load as TT
import anyconfig.query

from .common import BaseTestCase


@unittest.skipIf(not anyconfig.query.SUPPORTED,
                 'jmespath lib is not available')
class TestCase(BaseTestCase):
    kind = 'query'

    def test_single_load(self):
        for data in self.each_data():
            self.assertEqual(
                TT.single_load(
                    data.inp_path, ac_query=data.query.strip(), **data.opts
                ),
                data.exp,
                f'{data.datadir!s}, {data.inp_path!s}'
            )

    def test_single_load_with_invalid_query_string(self):
        for data in self.each_data():
            self.assertEqual(
                TT.single_load(
                    data.inp_path, ac_query=None, **data.opts
                ),
                TT.single_load(data.inp_path, **data.opts),
                f'{data.datadir!s}, {data.inp_path!s}'
            )

    def test_single_load_intentional_failures(self):
        for data in self.each_data():
            with self.assertRaises(AssertionError):
                exp = dict(z=1, zz='zz', zzz=[1, 2, 3], zzzz=dict(z=0))
                self.assertEqual(
                    TT.single_load(
                        data.inp_path, ac_query=data.query, **data.opts
                    ),
                    exp
                )

# vim:sw=4:ts=4:et:
