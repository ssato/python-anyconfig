#
# Copyright (C) 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
from __future__ import absolute_import

import unittest
import anyconfig.schema as TT
import anyconfig.compat


CNF_0 = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))
SCM_0 = {"type": "object",
         "properties": {
             "name": {"type": "string"},
             "a": {"type": "integer"},
             "b": {"type": "object",
                   "properties": {
                       "b": {"type": "array",
                             "items": {"type": "integer"}}}}}}


def dicts_equal(lhs, rhs):
    """
    >>> dicts_equal({}, {})
    True
    >>> dicts_equal({}, {'a': 1})
    False
    >>> d0 = {'a': 1}; dicts_equal(d0, d0)
    True
    >>> d1 = {'a': [1, 2, 3]}; dicts_equal(d1, d1)
    True
    >>> dicts_equal(d0, d1)
    False
    """
    if len(lhs.keys()) != len(rhs.keys()):
        return False

    for key, val in anyconfig.compat.iteritems(rhs):
        val_ref = lhs.get(key, None)
        if val != val_ref:
            return False

    return True


class Test(unittest.TestCase):

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

    def test_10__validate(self):
        self.assertTrue(TT.validate(self.obj, self.schema))

    def test_12__validate__ng(self):
        try:
            TT.validate({'a': "aaa"}, self.schema)
            assert False
        except TT.ValidationError:  # Validation should fail.
            pass

    def test_40_gen_schema__primitive_types(self):
        self.assertEquals(TT.gen_schema(0), {'type': 'integer'})
        self.assertEquals(TT.gen_schema("aaa"), {'type': 'string'})

        scm = TT.gen_schema([1])
        ref_scm = {'items': {'type': 'integer'}, 'type': 'array'}
        self.assertTrue(dicts_equal(scm, ref_scm))

        scm = TT.gen_schema({'a': 1})
        ref_scm = {'properties': {'a': {'type': 'integer'}}, 'type': 'object'}
        self.assertTrue(dicts_equal(scm, ref_scm))

    def test_42_gen_schema_and_validate(self):
        scm = TT.gen_schema(self.obj)
        self.assertTrue(TT.validate(self.obj, scm))

    def test_44_gen_schema__complex_types(self):
        scm = TT.gen_schema(self.obj2)
        self.assertTrue(dicts_equal(scm, self.ref_scm))

    def test_46_gen_schema_and_validate__complex_types(self):
        scm = TT.gen_schema(self.obj2)
        self.assertTrue(TT.validate(self.obj2, scm))

# vim:sw=4:ts=4:et:
