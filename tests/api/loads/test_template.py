#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest
import warnings

import anyconfig.api._load as TT
import anyconfig.template

from .common import BaseTestCase


@unittest.skipIf(not anyconfig.template.SUPPORTED,
                 'jinja2 template lib is not available')
class TestCase(BaseTestCase):

    kind = 'template'

    def test_loads_template(self):
        for data in self.each_data():
            inp = data.inp.read_text()
            ctx = TT.single_load(data.ctx, ac_parser='json')

            res = TT.loads(inp, ac_context=ctx, **data.opts)
            self.assertEqual(res, data.exp, f'{data.datadir!s}, {data.inp!s}')

    def test_loads_from_template_failures(self):
        inp = '{"a": "{{ a"}'
        with warnings.catch_warnings(record=True) as warns:
            warnings.simplefilter('always')
            res = TT.loads(inp, ac_parser='json', ac_template=True)
            self.assertEqual(res, dict(a='{{ a'))
            self.assertEqual(len(warns), 1)
            self.assertTrue(issubclass(warns[-1].category, UserWarning))

# vim:sw=4:ts=4:et:
