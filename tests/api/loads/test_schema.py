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

from .common import BaseTestCase


SCM_NG_0 = '{"type": "object", "properties": {"a": {"type": "string"}}}'


@unittest.skipIf(not anyconfig.schema.SUPPORTED,
                 'jsonschema lib is not available')
class TestCase(BaseTestCase):

    kind = 'schema'

    def test_loads_with_schema_validation(self):
        for data in self.each_data():
            scm = data.scm.read_text()
            (exp, opts) = (data.exp, data.opts)

            res = TT.loads(data.inp, ac_schema=scm, **opts)
            self.assertEqual(res, exp, f'{data.datadir!s}, {data.path!s}')

    def test_loads_with_schema_validation_failures(self):
        opts = dict(ac_parser='json', ac_schema=SCM_NG_0)

        for data in self.each_data(load=False):
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')

                res = TT.loads(data.inp, **opts)
                self.assertTrue(
                    res is None, f'{data.datadir!s}, {data.path!s}'
                )

            with self.assertRaises(ValidationError):
                TT.loads(data.inp, ac_schema_safe=False, **opts)

# vim:sw=4:ts=4:et:
