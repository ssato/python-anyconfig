#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.api._load as TT
import anyconfig.template

from .common import list_test_data


@unittest.skipIf(not anyconfig.template.SUPPORTED,
                 'jinja2 template lib is not available')
class TestCase(unittest.TestCase):

    def test_loads_template(self):
        for datadir, data in list_test_data('template'):
            for inp_path, _exp in data:
                ctx = TT.single_load(datadir / 'ctx' / inp_path.name)
                exp = TT.single_load(datadir / 'e' / inp_path.name)
                res = TT.loads(
                    inp_path.read_text(), ac_parser='json',
                    ac_template=True, ac_context=ctx
                )
                self.assertEqual(res, exp, f'{datadir!s}, {inp_path!s}')

    def test_loads_from_template_failures(self):
        inp = '{"a": "{{ a"}'
        res = TT.loads(inp, ac_parser='json', ac_template=True)
        self.assertEqual(res, dict(a='{{ a'))

# vim:sw=4:ts=4:et:
