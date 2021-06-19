#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import pathlib
import tempfile
import unittest
import warnings

import anyconfig.template

from . import common


@unittest.skipIf(not anyconfig.template.SUPPORTED,
                 'jinja2 template lib is not available')
class TestCase(common.TestCase):
    kind = 'template'
    pattern = '*.j2'

    def test_single_load(self):
        for data in self.each_data():
            self.assertEqual(
                self.target_fn(
                    data.inp_path, ac_context=data.ctx, **data.opts
                ),
                data.exp,
                f'{data.datadir!s}, {data.inp_path!s}'
            )

    def test_single_load_from_invalid_template(self):
        with tempfile.TemporaryDirectory() as tdir:
            wdir = pathlib.Path(tdir)
            inp = wdir / 'test.json'
            inp.write_text('{"a": "{{ a"}')  # broken template string.

            with warnings.catch_warnings(record=True) as warns:
                warnings.simplefilter('always')
                res = self.target_fn(
                    inp, ac_template=True, ac_context=dict(a=1)
                )
                self.assertEqual(res, dict(a='{{ a'))
                self.assertTrue(len(warns) > 0)
                self.assertTrue(issubclass(warns[-1].category, UserWarning))
                self.assertTrue('ailed to compile ' in str(warns[-1].message))

    def test_single_load_intentional_failures(self):
        ng_exp = dict(z=1, zz='zz', zzz=[1, 2, 3], zzzz=dict(z=0))
        for data in self.each_data():
            with self.assertRaises(AssertionError):
                self.assertEqual(
                    self.target_fn(
                        data.inp_path, ac_context=data.ctx, **data.opts
                    ),
                    ng_exp
                )

# vim:sw=4:ts=4:et:
