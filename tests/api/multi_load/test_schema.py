#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
import pathlib
import tempfile
import unittest

import anyconfig.schema

from anyconfig.api import ValidationError

from . import common


SCM_NG_0 = '{"type": "object", "properties": {"a": {"type": "string"}}}'


@unittest.skipIf(not anyconfig.schema.SUPPORTED,
                 'jsonschema lib is not available')
class TestCase(common.TestCase):
    kind = 'schema'

    def test_multi_load(self):
        for tdata in self.each_data():
            self.assertEqual(
                self.target_fn(
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
                    self.target_fn(
                        tdata.inputs, ac_schema=scm, ac_schema_safe=False
                    )

# vim:sw=4:ts=4:et:
