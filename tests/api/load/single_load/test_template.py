#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import pathlib
import unittest
import tempfile

import anyconfig.api._load as TT
import anyconfig.template

from .common import TestCaseWithExpctedData


@unittest.skipIf(not anyconfig.template.SUPPORTED,
                 'jinja2 template lib is not available')
class TemplateTestCase(TestCaseWithExpctedData):

    kind = 'template'

    def test_single_load_from_template(self):
        ices = (
            (inp,
             # see: tests/res/json/template/ctx/
             inp.parent / 'ctx' / inp.name,
             # see: tests/res/json/template/e/
             exp)
            for inp, exp in self.ies
        )
        for inp, ctx_path, exp_path in ices:
            ctx = TT.single_load(ctx_path)
            exp = TT.single_load(exp_path)
            res = TT.single_load(inp, ac_template=True, ac_context=ctx)
            self.assertEqual(res, exp, inp)

    def test_single_load_from_template_failures(self):
        with tempfile.TemporaryDirectory() as tdir:
            wdir = pathlib.Path(tdir)
            inp = wdir / 'test.json'
            inp.write_text('{"a": "{{ a"}')  # broken template string.

            self.assertEqual(
                TT.single_load(inp, ac_template=True, ac_context=dict(a=1)),
                dict(a='{{ a')
            )

# vim:sw=4:ts=4:et:
