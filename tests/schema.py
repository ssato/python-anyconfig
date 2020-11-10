#
# Copyright (C) 2015 - 2019 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, protected-access
# pylint: disable=bare-except
from __future__ import absolute_import, print_function

import unittest
import anyconfig.schema as TT


class Test_00_Base(unittest.TestCase):

    obj = {'a': 1}
    schema = {"type": "object",
              "properties": {"a": {"type": "integer"}}}

    obj2 = dict(a=1, b=[1, 2], c=dict(d="aaa", e=0.1))
    ref_scm = {'properties': {'a': {'type': 'integer'},
                              'b': {'items': {'type': 'integer'},
                                    'type': 'array'},
                              'c': {'properties': {'d': {'type': 'string'},
                                                   'e': {'type':
                                                         'number'}},
                                    'type': 'object'}},
               'type': 'object'}

    opts = dict(ac_schema_typemap=TT._SIMPLETYPE_MAP)


class Test_00_Functions(Test_00_Base):

    def test_20_array_to_schema(self):
        scm = TT.array_to_schema([1])
        ref = dict(items=dict(type="integer"), type="array")
        self.assertEqual(scm, ref, scm)

    def test_22_array_to_schema__empty_array(self):
        scm = TT.array_to_schema([])
        ref = dict(items=dict(type="string"), type="array")
        self.assertEqual(scm, ref, scm)

    def test_30_object_to_schema_nodes_iter(self):
        scm = TT.object_to_schema({'a': 1})
        ref = dict(type="object", properties=dict(a=dict(type="integer")))
        self.assertEqual(scm, ref, scm)


@unittest.skipIf(not TT.JSONSCHEMA_IS_AVAIL,
                 "json schema lib is not available")
class Test_10_Validation(Test_00_Base):

    def test_10_validate(self):
        (ret, msg) = TT.validate(self.obj, self.schema)
        self.assertFalse(msg)
        self.assertTrue(ret)

    def test_12_validate__ng(self):
        (ret, msg) = TT.validate({'a': "aaa"}, self.schema)
        self.assertTrue(msg)
        self.assertFalse(ret)

    def test_14_validate__ng_no_safe(self):
        self.assertRaises(Exception, TT.validate,
                          {'a': "aaa"}, self.schema, ac_schema_safe=False)


@unittest.skipIf(not TT.JSONSCHEMA_IS_AVAIL,
                 "json schema lib is not available")
class Test_12_Validation_Errors(Test_00_Base):

    obj = dict(a=1, b=2.0)
    scm = {"type": "object", "properties": {"a": {"type": "integer"},
                                            "b": {"type": "string"}}}

    def test_12_validate__ng(self):
        (ret, msg) = TT.validate(self.obj, self.scm, ac_schema_errors=True)
        self.assertTrue(msg)  # ["'a' is not of type ...", "'b' is not ..."]
        self.assertFalse(ret)


class Test_20_GenSchema(Test_00_Base):

    def test_40_gen_schema__primitive_types(self):
        self.assertEqual(TT.gen_schema(None), {'type': 'null'})
        self.assertEqual(TT.gen_schema(0), {'type': 'integer'})
        self.assertEqual(TT.gen_schema("aaa"), {'type': 'string'})

        scm = TT.gen_schema([1])
        ref_scm = {'items': {'type': 'integer'}, 'type': 'array'}
        self.assertEqual(scm, ref_scm)

        scm = TT.gen_schema({'a': 1})
        ref_scm = {'properties': {'a': {'type': 'integer'}}, 'type': 'object'}
        self.assertEqual(scm, ref_scm)

    def test_42_gen_schema_and_validate(self):
        scm = TT.gen_schema(self.obj)
        self.assertTrue(TT.validate(self.obj, scm))

    def test_44_gen_schema__complex_types(self):
        scm = TT.gen_schema(self.obj2)
        self.assertEqual(scm, self.ref_scm)

    def test_46_gen_schema_and_validate__complex_types(self):
        scm = TT.gen_schema(self.obj2)
        self.assertTrue(TT.validate(self.obj2, scm))


def _gen_scm(val):
    return TT.gen_schema(val, ac_schema_strict=True)


class Test_30_GenStrictSchema(Test_00_Base):

    schema = {"type": "object",
              "properties": {"a": {"type": "integer"}},
              "required": ["a"]}

    ref_scm = {'properties': {'a': {'type': 'integer'},
                              'b': {'items': {'type': 'integer'},
                                    'type': 'array',
                                    'minItems': 2, 'uniqueItems': True},
                              'c': {'properties': {'d': {'type': 'string'},
                                                   'e': {'type':
                                                         'number'}},
                                    'type': 'object',
                                    'required': ['d', 'e']}},
               'type': 'object',
               'required': ['a', 'b', 'c']}

    def test_40_gen_schema__primitive_types(self):
        self.assertEqual(_gen_scm(None), {'type': 'null'})
        self.assertEqual(_gen_scm(0), {'type': 'integer'})
        self.assertEqual(_gen_scm("aaa"), {'type': 'string'})

        scm = _gen_scm([1])
        ref_scm = {'items': {'type': 'integer'}, 'type': 'array',
                   'minItems': 1, 'uniqueItems': True}
        self.assertEqual(scm, ref_scm)

        scm = _gen_scm(["aaa", "bbb", "aaa"])
        ref_scm = {'items': {'type': 'string'}, 'type': 'array',
                   'minItems': 3, 'uniqueItems': False}
        self.assertEqual(scm, ref_scm)

        scm = _gen_scm({'a': 1})
        ref_scm = {'properties': {'a': {'type': 'integer'}},
                   'type': 'object', 'required': ['a']}
        self.assertEqual(scm, ref_scm)

    def test_42_gen_schema_and_validate(self):
        scm = _gen_scm(self.obj)
        self.assertTrue(TT.validate(self.obj, scm))

    def test_44_gen_schema__complex_types(self):
        scm = _gen_scm(self.obj2)
        self.assertEqual(scm, self.ref_scm)

    def test_46_gen_schema_and_validate__complex_types(self):
        scm = _gen_scm(self.obj2)
        self.assertTrue(TT.validate(self.obj2, scm))

# vim:sw=4:ts=4:et:
