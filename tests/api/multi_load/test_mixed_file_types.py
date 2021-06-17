#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import anyconfig.api._load as TT

from . import common


class TestCase(common.BaseTestCase):
    kind = 'mixed_types'
    pattern = '*.*'

    def test_multi_load_from_mixed_file_types_data(self):
        for tdata in self.each_data():
            self.assertEqual(
                TT.multi_load(tdata.inputs, **tdata.opts),
                tdata.exp,
                tdata
            )

# vim:sw=4:ts=4:et:
