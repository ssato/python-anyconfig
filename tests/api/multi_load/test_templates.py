#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.api._load as TT
import anyconfig.template

from . import common


@unittest.skipIf(not anyconfig.template.SUPPORTED,
                 'jinja2 template lib is not available')
class TestCase(common.BaseTestCase):
    kind = 'template'

    def test_multi_load_from_mixed_file_types_data(self):
        for tdata in self.each_data():
            self.assertEqual(
                TT.multi_load(
                    tdata.inputs, ac_context=tdata.ctx, **tdata.opts
                ),
                tdata.exp,
                tdata
            )

# vim:sw=4:ts=4:et:
