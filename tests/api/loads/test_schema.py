#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest
import warnings

import anyconfig.api._load as TT
import anyconfig.schema

from anyconfig.api import ValidationError

from . import common


SCM_NG_0 = '{"type": "object", "properties": {"a": {"type": "string"}}}'


@unittest.skipIf(not anyconfig.schema.SUPPORTED,
                 'jsonschema lib is not available')
class TestCase(common.TestCase):
    kind = 'schema'

    def test_loads_with_schema_validation(self):
        for data in self.each_data():
            scm = data.scm.read_text().strip()
            self.assertEqual(
                TT.loads(data.inp, ac_schema=scm, **data.opts),
                data.exp,
                f'{data.datadir!s}, {data.inp_path!s}'
            )

    def test_loads_with_schema_validation_failures(self):
        opts = dict(ac_parser='json', ac_schema=SCM_NG_0)

        for data in self.each_data():
            with warnings.catch_warnings(record=True) as warns:
                warnings.simplefilter('always')
                self.assertTrue(
                    TT.loads(data.inp, **opts) is None,
                    f'{data.datadir!s}, {data.inp_path!s}'
                )
                self.assertTrue(len(warns) > 0)
                self.assertTrue(issubclass(warns[-1].category, UserWarning))

            with self.assertRaises(ValidationError):
                TT.loads(data.inp, ac_schema_safe=False, **opts)

# vim:sw=4:ts=4:et:
