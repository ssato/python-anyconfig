#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import ast
import collections
import pathlib

import anyconfig.api._load as TT

from anyconfig.api import (
    UnknownFileTypeError, UnknownProcessorTypeError
)
from tests.base import NULL_CNTNR

from .common import BaseTestCase


class MyDict(collections.OrderedDict):
    """My original dict class keep key orders."""
    pass


class TestCase(BaseTestCase):

    def test_single_load(self):
        for inp, exp in self.ies:
            self.assertEqual(TT.single_load(inp), exp)

    def test_single_load_failiure_unknown_file_type(self):
        with self.assertRaises(UnknownFileTypeError):
            TT.single_load('dummy.ext_not_exist')

    def test_single_load_failiure_unknown_processor_type(self):
        with self.assertRaises(UnknownProcessorTypeError):
            TT.single_load('dummy.txt', ac_parser='proc_does_not_exist')

    def test_single_load_failiure_invalid_object(self):
        with self.assertRaises(ValueError):
            TT.single_load('dummy.txt', ac_parser=object())

    def test_single_load_failiure_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            TT.single_load('not_exist.json')

    def test_single_load_from_stream(self):
        for inp, exp in self.ies:
            res = TT.single_load(open(inp), ac_parser='json')
            self.assertEqual(res, exp)

    def test_single_load_from_path_str(self):
        for inp, exp in self.ies:
            res = TT.single_load(str(inp), ac_parser='json')
            self.assertEqual(res, exp)

    def test_single_load_with_ac_parser_by_str(self):
        for inp, exp in self.ies:
            self.assertEqual(TT.single_load(inp, ac_parser='json'), exp)

    def test_single_load_with_ac_parser_by_instance(self):
        for inp, exp in self.ies:
            res = TT.single_load(inp, ac_parser=self.psr)
            self.assertEqual(res, exp)

    def test_single_load_with_ac_parser_by_id(self):
        for inp, exp in self.ies:
            res = TT.single_load(inp, ac_parser=self.psr.cid())
            self.assertEqual(res, exp)

    def test_single_load_ignore_missing(self):
        inp = pathlib.Path(__file__).parent / 'conf_file_not_exist.json'
        assert not inp.exists()

        res = TT.single_load(inp, ac_parser='json', ac_ignore_missing=True)
        self.assertEqual(res, NULL_CNTNR)

    def test_single_load_with_ac_ordered(self):
        for inp, exp in self.ies:
            res = TT.single_load(inp, ac_ordered=True)
            self.assertEqual(res, collections.OrderedDict(exp))

    def test_single_load_with_ac_dict(self):
        for inp, exp in self.ies:
            res = TT.single_load(inp, ac_dict=MyDict)
            self.assertTrue(isinstance(res, MyDict))
            self.assertEqual(res, exp)


class PrimitivesTestCase(BaseTestCase):

    kind = 'primitives'

    def test_single_load_primitive_data(self):
        ies = (
            (inp,
             # see: tests/res/json/basic/primitives/e/
             inp.parent / 'e' / inp.name.replace('.json', '.txt')
             )
            for inp, _exp in self.ies
        )
        for inp, exp_path in ies:
            exp = ast.literal_eval(exp_path.read_text().strip())
            self.assertEqual(TT.single_load(inp), exp)

# vim:sw=4:ts=4:et:
