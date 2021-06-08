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

    def test_multi_load_with_query(self):
        iqes = (
            (rdir,
             sorted(rdir.glob('*.json')),   # inputs
             (rdir / 'q' / 'q.txt').read_text().strip(),
             exp,
             opts)
            for rdir, exp, opts in self.datasets
        )

        for rdir, inputs, query, exp, opts in iqes:
            res = TT.multi_load(inputs, ac_query=query)
            self.assertEqual(res, exp, f'{rdir!s}')

# vim:sw=4:ts=4:et:
