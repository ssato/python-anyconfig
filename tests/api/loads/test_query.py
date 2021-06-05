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
            query = data.query.read_text()
            res = TT.loads(data.inp, ac_query=query, **data.opts)
            self.assertEqual(res, data.exp, f'{data.datadir!s}, {data.path!s}')

    def test_loads_with_invalid_query(self):
        opts = dict(ac_parser='json')

        for data in self.each_data(load=False):
            self.assertEqual(
                TT.loads(data.inp, ac_query=None, **opts),
                TT.single_load(data.path),
                f'{data.datadir!s}, {data.path!s}'
            )

# vim:sw=4:ts=4:et:
