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
        for inp, exp in self.list_inp_exp:
            query = (
                self.root / 'q' / inp.name.replace('.json', '.txt')
            ).read_text().strip()

            res = TT.loads(inp.read_text(), ac_parser='json', ac_query=query)
            self.assertEqual(res, exp)

    def test_loads_with_invalid_query(self):
        for inp, _exp in self.list_inp_exp:
            inp_s = inp.read_text()
            self.assertEqual(
                TT.loads(inp_s, ac_parser='json', ac_query=None),
                TT.loads(inp_s, ac_parser='json'),
                inp
            )

# vim:sw=4:ts=4:et:
