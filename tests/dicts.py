#
# Forked from m9dicts.tests.{api,dicts}
#
# Copyright (C) 2011 - 2019 Satoru SATOH <satoru.satoh@gmail.com>
#
# pylint: disable=missing-docstring,invalid-name,protected-access
# pylint: disable=ungrouped-imports
from __future__ import absolute_import

import copy
import unittest

from collections import OrderedDict

import anyconfig.dicts as TT

from anyconfig.utils import is_dict_like


class Test_10_get(unittest.TestCase):

    def test_10_empty_path(self):
        dic = dict(a=1, b=[1, 2])
        (dic2, err) = TT.get(dic, '')
        self.assertEqual(err, '')
        self.assertEqual(dic2, dic)

    def test_20_json_pointer(self):
        # test case in rfc, http://tools.ietf.org/html/rfc6901
        dic = {"foo": ["bar", "baz"],
               "": 0,
               "a/b": 1,
               "c%d": 2,
               "e^f": 3,
               "g|h": 4,
               r"i\\j": 5,
               r'k\"l': 6,
               " ": 7,
               "m~n": 8}

        self.assertTrue(TT.get(dic, "")[0], dic)
        self.assertEqual(TT.get(dic, "/foo")[0], ["bar", "baz"])
        self.assertEqual(TT.get(dic, "/foo/0")[0], "bar")
        self.assertEqual(TT.get(dic, "/")[0], 0)
        self.assertEqual(TT.get(dic, "/a~1b")[0], 1)
        self.assertEqual(TT.get(dic, "/c%d")[0], 2)
        self.assertEqual(TT.get(dic, "/e^f")[0], 3)
        self.assertEqual(TT.get(dic, "/g|h")[0], 4)
        self.assertEqual(TT.get(dic, r"/i\\j")[0], 5)
        self.assertEqual(TT.get(dic, r'/k\"l')[0], 6)
        self.assertEqual(TT.get(dic, "/ ")[0], 7)
        self.assertEqual(TT.get(dic, "/m~0n")[0], 8)

    def test_22_json_pointer__array(self):
        dic = dict(a=[1, 2], )
        self.assertEqual(TT.get(dic, "/a/1"), (2, ''))

        (val, msg) = TT.get(dic, "/a/2")
        self.assertTrue(val is None)
        self.assertTrue(bool(msg))
        # maybe the error message depends on python version.
        # self.assertEqual(msg, 'list index out of range')

        (val, msg) = TT.get(dic, "/a/b/d/-")
        self.assertTrue(val is None)
        self.assertTrue(bool(msg))
        # Likewise.
        # self.assertEqual(msg, 'list indices must be integers...')


class Test_10_update_with_replace(unittest.TestCase):

    ac_merge = TT.MS_REPLACE

    dic = OrderedDict((("a", 1), ("b", [1, 3]), ("c", "abc"), ("f", None)))
    other = OrderedDict((("a", 2), ("b", [0, 1]),
                         ("c", OrderedDict((("d", "d"), ("e", 1)))),
                         ("d", "d")))

    def assert_dicts_equal(self, dic, upd, ref):
        if not is_dict_like(upd):
            upd = OrderedDict(upd)

        self.assertTrue(all(dic[k] == upd[k] for k in upd.keys()))
        self.assertTrue(all(dic[k] == ref[k] for k in ref.keys()
                            if k not in upd))

    def assert_updated(self, other):
        dic = copy.deepcopy(self.dic)
        TT.merge(dic, other, ac_merge=self.ac_merge)
        self.assert_dicts_equal(dic, other, self.dic)

    def test_10_update_with_a_odict(self):
        self.assert_updated(self.other)

    def test_12_update_with_a_dict(self):
        self.assert_updated(dict(self.other))

    def test_20_update_with_iterable(self):
        self.assert_updated(self.other.items())

    def test_30_update_with_invalid(self):
        self.assertRaises((ValueError, TypeError), TT.merge, self.dic, 1)


class Test_20_update_wo_replace(Test_10_update_with_replace):

    ac_merge = TT.MS_NO_REPLACE

    def assert_dicts_equal(self, dic, upd, ref):
        if not is_dict_like(upd):
            upd = OrderedDict(upd)

        self.assertTrue(all(dic[k] == upd[k] for k in upd.keys()
                            if k not in ref))
        self.assertTrue(all(dic[k] == ref[k] for k in ref.keys()))


class Test_30_update_with_merge(Test_10_update_with_replace):

    ac_merge = TT.MS_DICTS
    replaced_keys = "a b d".split()

    def assert_dicts_equal(self, dic, upd, ref):
        if not is_dict_like(upd):
            upd = OrderedDict(upd)

        self.assertTrue(all(dic[k] == upd[k] for k in self.replaced_keys))
        self.assertTrue(all(dic["c"][k] == upd["c"][k] for k
                            in upd["c"].keys()))
        self.assertTrue(all(dic[k] == ref[k] for k in ref.keys()
                            if k not in upd))


class Test_32_update_with_merge_lists(Test_10_update_with_replace):

    ac_merge = TT.MS_DICTS_AND_LISTS

    def assert_dicts_equal(self, dic, upd, ref):
        if not is_dict_like(upd):
            upd = OrderedDict(upd)

        self.assertTrue(all(dic[k] == upd[k] for k in ["d"]))
        self.assertEqual(dic["c"], upd["c"])  # Overwritten.
        self.assertTrue(all(dic[k] == ref[k] for k in ref.keys()
                            if k not in upd))


class Test_40_merge(unittest.TestCase):

    dic = dict(a=1, b=dict(b=[0, 1], c="C"), name="a")
    upd = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"), e="E")

    def test_10_update_with_replace(self):
        dic = copy.deepcopy(self.dic)
        exp = copy.deepcopy(self.upd)
        exp["name"] = dic["name"]

        TT.merge(dic, self.upd, ac_merge=TT.MS_REPLACE)
        self.assertEqual(dic, exp)

    def test_20_update_wo_replace(self):
        dic = copy.deepcopy(self.dic)
        exp = copy.deepcopy(self.dic)
        exp["e"] = self.upd["e"]

        TT.merge(dic, self.upd, ac_merge=TT.MS_NO_REPLACE)
        self.assertEqual(dic, exp)

    def test_30_update_with_merge(self):
        dic = copy.deepcopy(self.dic)
        exp = copy.deepcopy(self.upd)
        exp["b"]["c"] = dic["b"]["c"]
        exp["name"] = dic["name"]

        TT.merge(dic, self.upd, ac_merge=TT.MS_DICTS)
        self.assertEqual(dic, exp)

    def test_40_update_with_merge_lists(self):
        dic = copy.deepcopy(self.dic)
        exp = copy.deepcopy(self.upd)
        exp["b"]["b"] = [0] + exp["b"]["b"]
        exp["b"]["c"] = dic["b"]["c"]
        exp["name"] = dic["name"]

        TT.merge(dic, self.upd, ac_merge=TT.MS_DICTS_AND_LISTS)
        self.assertEqual(dic, exp)

    def test_50_update_with_custom_merge(self):
        def set_none_merge_strat(self, other, key, *args, **kwargs):
            for k in self:
                self[k] = None

        dic = copy.deepcopy(self.dic)
        exp = dict(zip(dic.keys(), [None for _ in dic]))

        TT.merge(dic, self.upd, ac_merge=set_none_merge_strat)
        self.assertEqual(dic, exp)

# vim:sw=4:ts=4:et:
