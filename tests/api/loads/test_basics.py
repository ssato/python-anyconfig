#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.api._load as TT
import anyconfig.api

from .common import list_test_data


class TestCase(unittest.TestCase):

    def test_loads(self):
        for datadir, data in list_test_data():
            for inp_path, exp in data:
                res = TT.loads(inp_path.read_text(), ac_parser='json')
                self.assertEqual(res, exp, f'{datadir!s}, {inp_path!s}')

    def test_loads_failures(self):
        for datadir, data in list_test_data('errors'):
            ioees = sorted(
                (inp.read_text(),  # input as a string
                 TT.single_load(inp.parent / 'options' / '00.json'),  # options
                 TT.single_load(inp.parent / 'e' / 'exp.json'),  # expected...
                 sorted(  # exceptions
                    e.name for e in (inp.parent / 'exc').glob('*')
                 ),
                 )
                for inp, _exp in data
            )

            for inp, opts, exp, excs in ioees:
                if excs:
                    exc = getattr(anyconfig.api, excs[0], None)
                    if exc:
                        with self.assertRaises(exc):
                            TT.loads(inp, **opts)
                else:
                    res = TT.loads(inp, **opts)
                    self.assertEqual(res, exp, f'{datadir!s}')

# vim:sw=4:ts=4:et:
