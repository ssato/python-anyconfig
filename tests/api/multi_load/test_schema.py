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

from . import common


SCM_NG_0 = '{"type": "object", "properties": {"a": {"type": "string"}}}'


@unittest.skipIf(not anyconfig.schema.SUPPORTED,
                 'jsonschema lib is not available')
class TestCase(common.BaseTestCase):
    kind = 'schema'

    def test_multi_load_with_schema_validation(self):
        for tdata in self.each_data():
            self.assertEqual(
                TT.multi_load(
                    tdata.inputs, ac_schema=tdata.scm, **tdata.opts
                ),
                tdata.exp,
                tdata
            )

    def test_multi_load_with_schema_validation_failure(self):
        with tempfile.TemporaryDirectory() as tdir:
            wdir = pathlib.Path(tdir)
            scm = wdir / 'scm.json'
            scm.write_text(SCM_NG_0)

            for tdata in self.each_data():
                with self.assertRaises(ValidationError):
                    TT.multi_load(
                        tdata.inputs, ac_schema=scm, ac_schema_safe=False
                    )

# vim:sw=4:ts=4:et:
