#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import anyconfig.api._load as TT

from .common import BaseTestCase


class TestCase(BaseTestCase):

    kind = 'mixed_types'

    def test_multi_load_from_mixed_file_types_data(self):
        for rdir, exp, opts in self.datasets:
            res = TT.multi_load(sorted(rdir.glob('*.*')), **opts)
            self.assertEqual(res, exp, f'{rdir!s}')

# vim:sw=4:ts=4:et:
