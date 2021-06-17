#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import pathlib
import tempfile
import unittest
import warnings

import anyconfig.api._load as TT
import anyconfig.schema

from anyconfig.api import ValidationError

from . import common


SCM_NG_0 = '{"type": "object", "properties": {"a": {"type": "string"}}}'


@unittest.skipIf(not anyconfig.schema.SUPPORTED,
                 'jsonschema lib is not available')
class TestCase(common.BaseTestCase):
    kind = 'schema'

    def test_single_load(self):
        for data in self.each_data():
            self.assertEqual(
                TT.single_load(
                    data.inp_path, ac_schema=data.scm, **data.opts
                ),
                data.exp,
                f'{data.datadir!s}, {data.inp_path!s}'
            )

    def test_single_load_with_validateion_failures(self):
        with tempfile.TemporaryDirectory() as tdir:
            wdir = pathlib.Path(tdir)
            scm = wdir / 'scm.json'
            scm.write_text(SCM_NG_0)

            for data in self.each_data():
                with warnings.catch_warnings(record=True) as warns:
                    warnings.simplefilter('always')
                    self.assertEqual(
                        TT.single_load(
                            data.inp_path, ac_schema=scm, ac_schema_safe=True,
                            **data.opts
                        ),
                        None
                    )
                    self.assertTrue(len(warns) > 0)
                    self.assertTrue(
                        issubclass(warns[-1].category, UserWarning)
                    )
                    self.assertTrue('scm=' in str(warns[-1].message))

                with self.assertRaises(ValidationError):
                    TT.single_load(
                        data.inp_path, ac_schema=scm, ac_schema_safe=False
                    )

# vim:sw=4:ts=4:et:
