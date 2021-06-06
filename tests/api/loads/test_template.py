#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest
import warnings

import anyconfig.api._load as TT
import anyconfig.template

from . import common


@unittest.skipIf(not anyconfig.template.SUPPORTED,
                 'jinja2 template lib is not available')
class TestCase(common.BaseTestCase):
    kind = 'template'

    def test_loads_template(self):
        for data in self.each_data():
            self.assertEqual(
                TT.loads(data.inp, ac_context=data.ctx, **data.opts),
                data.exp,
                f'{data.datadir!s}, {data.inp_path!s}'
            )

    def test_loads_from_template_failures(self):
        inp = '{"a": "{{ a"}'
        with warnings.catch_warnings(record=True) as warns:
            warnings.simplefilter('always')
            res = TT.loads(inp, ac_parser='json', ac_template=True)
            self.assertEqual(res, dict(a='{{ a'))
            # self.assertEqual(len(warns), 1)  # Needs to fix plugins
            self.assertTrue(issubclass(warns[-1].category, UserWarning))

# vim:sw=4:ts=4:et:
