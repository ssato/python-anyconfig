#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import collections
import pathlib

import anyconfig.api._load as TT
import anyconfig.parsers

from anyconfig.api import (
    UnknownFileTypeError, UnknownProcessorTypeError
)
from ... import base
from . import common


JSON_PARSER = anyconfig.parsers.find(None, 'json')


class MyDict(collections.OrderedDict):
    """My original dict class keep key orders."""


class TestCase(common.TestCase):

    def test_single_load_from_stream(self):
        for data in self.each_data():
            self.assertEqual(
                TT.single_load(data.inp_path.open(), **data.opts),
                data.exp
            )

    def test_single_load_from_path_str(self):
        for data in self.each_data():
            self.assertEqual(
                TT.single_load(str(data.inp_path), **data.opts),
                data.exp
            )

    def test_single_load_with_ac_parser_by_instance(self):
        for data in self.each_data():
            self.assertEqual(
                TT.single_load(data.inp_path, ac_parser=JSON_PARSER),
                data.exp
            )

    def test_single_load_with_ac_parser_by_id(self):
        for data in self.each_data():
            self.assertEqual(
                TT.single_load(data.inp_path, ac_parser=JSON_PARSER.cid()),
                data.exp
            )

    def test_single_load_with_ac_ordered(self):
        for data in self.each_data():
            self.assertEqual(
                TT.single_load(data.inp_path, ac_ordered=True),
                collections.OrderedDict(data.exp)
            )

    def test_single_load_with_ac_dict(self):
        for data in self.each_data():
            res = TT.single_load(data.inp_path, ac_dict=MyDict)
            self.assertTrue(isinstance(res, MyDict))
            self.assertEqual(res, MyDict(**data.exp))

    def test_single_load_missing_file_failures(self):
        with self.assertRaises(FileNotFoundError):
            TT.single_load('not_exist.json')

    def test_single_load_unknown_file_type_failures(self):
        with self.assertRaises(UnknownFileTypeError):
            TT.single_load('dummy.txt')

    def test_single_load_invalid_parser_object_failures(self):
        with self.assertRaises(ValueError):
            TT.single_load('dummy.txt', ac_parser=object())

    def test_single_load_unknown_processor_type_failures(self):
        for data in self.each_data():
            with self.assertRaises(UnknownProcessorTypeError):
                TT.single_load(
                    data.inp_path, ac_parser='proc_does_not_exist'
                )

    def test_single_load_ignore_missing(self):
        inp = pathlib.Path() / 'conf_file_not_exist.json'
        assert not inp.exists()

        res = TT.single_load(inp, ac_parser='json', ac_ignore_missing=True)
        self.assertEqual(res, base.NULL_CNTNR)

# vim:sw=4:ts=4:et:
