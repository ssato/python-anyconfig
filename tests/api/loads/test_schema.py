#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.api._load as TT
import anyconfig.schema

from anyconfig.api import ValidationError

from .common import list_test_data


SCM_NG_0 = '{"type": "object", "properties": {"a": {"type": "string"}}}'


@unittest.skipIf(not anyconfig.schema.SUPPORTED,
                 'jsonschema lib is not available')
class TestCase(unittest.TestCase):

    def test_loads_with_schema_validation(self):
        for datadir, data in list_test_data('schema'):
            for inp_path, exp in data:
                scm = (inp_path.parent / 'schema' / inp_path.name).read_text()
                res = TT.loads(
                    inp_path.read_text(), ac_parser='json', ac_schema=scm
                )
                self.assertEqual(res, exp, f'{datadir!s}, {inp_path!s}')

    def test_loads_with_schema_validation_failures(self):
        opts = dict(ac_parser='json', ac_schema=SCM_NG_0)

        for datadir, data in list_test_data('schema'):
            for inp_path, _exp in data:
                inp = inp_path.read_text()

                res = TT.loads(inp, **opts)
                self.assertTrue(res is None, f'{datadir!s}, {inp_path!s}')

                with self.assertRaises(ValidationError):
                    TT.loads(inp, ac_schema_safe=False, **opts)

# vim:sw=4:ts=4:et:
