#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import collections

import anyconfig.api._load as TT

from ...base import NULL_CNTNR
from . import common


class MyDict(collections.OrderedDict):
    pass


class TestCase(common.BaseTestCase):

    def test_multi_load_from_empty_path_list(self):
        self.assertEqual(TT.multi_load([]), NULL_CNTNR)

    def test_multi_load_from_path_objects(self):
        for tdata in self.each_data():
            self.assertEqual(
                TT.multi_load(tdata.inputs, **tdata.opts),
                tdata.exp
            )

    def test_multi_load_from_glob_path_str(self):
        for tdata in self.each_data():
            self.assertEqual(
                TT.multi_load((str(i) for i in tdata.inputs), **tdata.opts),
                tdata.exp
            )

    def test_multi_load_from_streams(self):
        for tdata in self.each_data():
            self.assertEqual(
                TT.multi_load((i.open() for i in tdata.inputs), **tdata.opts),
                tdata.exp
            )

    def test_multi_load_to_ac_dict(self):
        for tdata in self.each_data():
            res = TT.multi_load(tdata.inputs, ac_dict=MyDict, **tdata.opts)
            self.assertEqual(res, tdata.exp, tdata)
            self.assertTrue(isinstance(res, MyDict))

    def test_multi_load_with_wrong_merge_strategy(self):
        for tdata in self.each_data():
            with self.assertRaises(ValueError):
                TT.multi_load(tdata.inputs, ac_merge='wrong_merge_strategy')

    def test_multi_load_with_ignore_missing_option(self):
        paths = [
            'file_not_exist_0.json',
            'file_not_exist_1.json',
            'file_not_exist_2.json',
        ]
        with self.assertRaises(FileNotFoundError):
            TT.multi_load(paths)

        self.assertEqual(
            TT.multi_load(paths, ac_ignore_missing=True),
            NULL_CNTNR
        )

# vim:sw=4:ts=4:et:
