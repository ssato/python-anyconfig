#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.template

from . import common


@unittest.skipIf(not anyconfig.template.SUPPORTED,
                 'jinja2 template lib is not available')
class TestCase(common.TestCase):
    kind = 'template'

    def test_multi_load(self):
        for tdata in self.each_data():
            self.assertEqual(
                self.target_fn(
                    tdata.inputs, ac_context=tdata.ctx, **tdata.opts
                ),
                tdata.exp,
                tdata
            )

    def test_multi_load_failures(self):
        for tdata in self.each_data():
            with self.assertRaises(AssertionError):
                self.assertEqual(
                    self.target_fn(
                        tdata.inputs, ac_context=tdata.ctx, **tdata.opts
                    ),
                    None,
                    tdata
                )

# vim:sw=4:ts=4:et:
