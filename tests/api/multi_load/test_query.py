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
    should_exist = ('e', 'q')

    def test_multi_load(self):
        for tdata in self.each_data():
            self.assertEqual(
                self.target_fn(
                    tdata.inputs, ac_query=tdata.query, **tdata.opts
                ),
                tdata.exp
            )

    def test_multi_load_with_invalid_query(self):
        for tdata in self.each_data():
            self.assertEqual(
                self.target_fn(tdata.inputs, ac_query='', **tdata.opts),
                self.target_fn(tdata.inputs)
            )

# vim:sw=4:ts=4:et:
