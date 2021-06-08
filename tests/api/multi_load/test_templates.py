#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.api._load as TT
import anyconfig.template

from .common import BaseTestCase


@unittest.skipIf(not anyconfig.template.SUPPORTED,
                 'jinja2 template lib is not available')
class TestCase(BaseTestCase):

    kind = 'templates'

    def test_multi_load_from_mixed_file_types_data(self):
        ices = (
            (rdir,
             sorted(rdir.glob('*.json')),   # inputs
             TT.single_load(rdir / 'ctx' / '00.json'),  # context object
             exp,
             opts)
            for rdir, exp, opts in self.datasets
        )

        for rdir, inputs, ctx, exp, opts in ices:
            res = TT.multi_load(
                inputs, ac_template=True, ac_context=ctx, **opts
            )
            self.assertEqual(res, exp, f'{rdir!s}')

# vim:sw=4:ts=4:et:
