#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.api._load as TT
import anyconfig.query

from . import common


@unittest.skipIf(not anyconfig.query.SUPPORTED,
                 'jmespath lib is not available')
class TestCase(common.BaseTestCase):
    kind = 'query'
    should_exist = ('e', 'q')

    def test_multi_load_with_invalid_query(self):
        for tdata in self.each_data():
            self.assertEqual(
                TT.multi_load(tdata.inputs, ac_query='', **tdata.opts),
                TT.multi_load(tdata.inputs)
            )

    def test_multi_load_with_query(self):
        for tdata in self.each_data():
            self.assertEqual(
                TT.multi_load(
                    tdata.inputs, ac_query=tdata.query, **tdata.opts
                ),
                tdata.exp
            )

# vim:sw=4:ts=4:et:
