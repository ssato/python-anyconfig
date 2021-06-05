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

    def test_loads_with_query(self):
        for data in self.each_data():
            inp = data.inp.read_text()
            query = data.query.read_text()

            res = TT.loads(inp, ac_query=query, **data.opts)
            self.assertEqual(res, data.exp, f'{data.datadir!s}, {data.inp!s}')

    def test_loads_with_invalid_query(self):
        opts = dict(ac_parser='json')

        for data in self.each_data(load=False):
            inp = data.inp.read_text()
            self.assertEqual(
                TT.loads(inp, ac_query=None, **opts),
                TT.single_load(data.inp),
                f'{data.datadir!s}, {data.inp!s}'
            )

# vim:sw=4:ts=4:et:
