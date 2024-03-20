#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
import collections

from ... import base
from . import common


class MyDict(collections.OrderedDict):
    pass


class TestCase(common.TestCase):

    def test_multi_load_from_empty_path_list(self):
        self.assertEqual(self.target_fn([]), base.NULL_CNTNR)

    def test_multi_load_from_glob_path_str(self):
        for tdata in self.each_data():
            self.assertEqual(
                self.target_fn((str(i) for i in tdata.inputs), **tdata.opts),
                tdata.exp
            )

    def test_multi_load_from_streams(self):
        for tdata in self.each_data():
            self.assertEqual(
                self.target_fn((i.open() for i in tdata.inputs), **tdata.opts),
                tdata.exp
            )

    def test_multi_load_to_ac_dict(self):
        for tdata in self.each_data():
            res = self.target_fn(tdata.inputs, ac_dict=MyDict, **tdata.opts)
            self.assertEqual(res, tdata.exp, tdata)
            self.assertTrue(isinstance(res, MyDict))

    def test_multi_load_with_wrong_merge_strategy(self):
        for tdata in self.each_data():
            with self.assertRaises(ValueError):
                self.target_fn(tdata.inputs, ac_merge='wrong_merge_strategy')

    def test_multi_load_with_ignore_missing_option(self):
        paths = [
            'file_not_exist_0.json',
            'file_not_exist_1.json',
            'file_not_exist_2.json',
        ]
        with self.assertRaises(FileNotFoundError):
            self.target_fn(paths)

        self.assertEqual(
            self.target_fn(paths, ac_ignore_missing=True),
            base.NULL_CNTNR
        )

# vim:sw=4:ts=4:et:
