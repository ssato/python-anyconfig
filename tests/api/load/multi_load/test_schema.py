#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import pathlib
import tempfile
import unittest

import anyconfig.api._load as TT
import anyconfig.schema

from anyconfig.api import ValidationError

from .common import BaseTestCase


SCM_NG_0 = '{"type": "object", "properties": {"a": {"type": "string"}}}'


@unittest.skipIf(not anyconfig.schema.SUPPORTED,
                 'jsonschema lib is not available')
class TestCase(BaseTestCase):

    kind = 'schema'

    def test_multi_load_with_schema_validation(self):
        ices = (
            (rdir,
             sorted(rdir.glob('*.json')),   # inputs
             rdir / 'scm' / '00.json',
             exp,
             opts)
            for rdir, exp, opts in self.datasets
        )

        for rdir, inputs, scm, exp, opts in ices:
            res = TT.multi_load(inputs, ac_schema=scm, **opts)
            self.assertEqual(res, exp, f'{rdir!s}')

    def test_multi_load_with_schema_validation_failure(self):
        with tempfile.TemporaryDirectory() as tdir:
            wdir = pathlib.Path(tdir)
            scm = wdir / 'scm.json'
            scm.write_text(SCM_NG_0)

            inputs = [
                sorted(rdir.glob('*.json'))
                for rdir, _exp, _opts in self.datasets
            ]
            with self.assertRaises(ValidationError):
                TT.multi_load(inputs[0], ac_schema=scm, ac_schema_safe=False)

# vim:sw=4:ts=4:et:
