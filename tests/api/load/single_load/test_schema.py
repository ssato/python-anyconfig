#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
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
class ValidationTestCase(BaseTestCase):

    def test_single_load_with_validation(self):
        ises = (
            (inp,
             # see: tests/res/json/basic/schema/
             inp.parent / 'schema' / inp.name,
             exp)
            for inp, exp in self.ies
        )
        for inp, scm, exp in ises:
            self.assertEqual(TT.single_load(inp, ac_schema=scm), exp)

    def test_single_load_with_validation_failures(self):
        with tempfile.TemporaryDirectory() as tdir:
            wdir = pathlib.Path(tdir)
            scm_path = wdir / 'scm.json'
            scm_path.write_text(SCM_NG_0)
            scm = TT.single_load(scm_path)

            for inp, _exp in self.ies:
                self.assertEqual(
                    TT.single_load(inp, ac_schema=scm, ac_schema_safe=True),
                    None
                )
                with self.assertRaises(ValidationError):
                    TT.single_load(inp, ac_schema=scm, ac_schema_safe=False)

# vim:sw=4:ts=4:et:
