#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.api._load as TT
import anyconfig.query

from . import common


@unittest.skipIf(not anyconfig.query.SUPPORTED,
                 'jmespath lib is not available')
class TestCase(common.TestCase):
    kind = 'query'

    def test_loads_with_query(self):
        for data in self.each_data():
            self.assertEqual(
                TT.loads(data.inp, ac_query=data.query, **data.opts),
                data.exp,
                f'{data.datadir!s}, {data.inp_path!s}'
            )

    def test_loads_with_invalid_query(self):
        opts = dict(ac_parser='json')
        for data in self.each_data():
            self.assertEqual(
                TT.loads(data.inp, ac_query=None, **opts),
                TT.single_load(data.inp_path, **opts),
                f'{data.datadir!s}, {data.inp_path!s}'
            )

# vim:sw=4:ts=4:et:
