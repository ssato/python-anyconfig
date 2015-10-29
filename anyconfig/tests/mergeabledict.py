#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato @ redhat.com>
#
# pylint: disable=missing-docstring,invalid-name
from __future__ import absolute_import

import unittest
import anyconfig.mergeabledict as TT

from anyconfig.tests.common import dicts_equal


class Test00Functions(unittest.TestCase):

    def test_10_create_from__convert_to(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"), e=[3, 4])
        b = TT.create_from(a)
        c = TT.convert_to(b)

        self.assertTrue(isinstance(b, TT.MergeableDict))
        self.assertTrue(isinstance(c, dict))
        self.assertFalse(isinstance(c, TT.MergeableDict))

    def test_20_get__invalid_inputs(self):
        dic = dict(a=1, b=[1, 2])
        (dic2, err) = TT.get(dic, '')
        self.assertEquals(err, '')
        self.assertTrue(dicts_equal(dic2, dic))

    def test_22_get__json_pointer(self):
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

        self.assertTrue(dicts_equal(TT.get(dic, "")[0], dic))
        self.assertEquals(TT.get(dic, "/foo")[0], ["bar", "baz"])
        self.assertEquals(TT.get(dic, "/foo/0")[0], "bar")
        self.assertEquals(TT.get(dic, "/")[0], 0)
        self.assertEquals(TT.get(dic, "/a~1b")[0], 1)
        self.assertEquals(TT.get(dic, "/c%d")[0], 2)
        self.assertEquals(TT.get(dic, "/e^f")[0], 3)
        self.assertEquals(TT.get(dic, "/g|h")[0], 4)
        self.assertEquals(TT.get(dic, r"/i\\j")[0], 5)
        self.assertEquals(TT.get(dic, r'/k\"l')[0], 6)
        self.assertEquals(TT.get(dic, "/ ")[0], 7)
        self.assertEquals(TT.get(dic, "/m~0n")[0], 8)

    def test_24_get__json_pointer__array(self):
        dic = dict(a=[1, 2], )
        self.assertEquals(TT.get(dic, "/a/1"), (2, ''))

        (val, msg) = TT.get(dic, "/a/2")
        self.assertTrue(val is None)
        self.assertTrue(bool(msg))
        # maybe the error message depends on python version.
        # self.assertEquals(msg, 'list index out of range')

        (val, msg) = TT.get(dic, "/a/b/d/-")
        self.assertTrue(val is None)
        self.assertTrue(bool(msg))
        # Likewise.
        # self.assertEquals(msg, 'list indices must be integers...')


class Test10MergeableDict(unittest.TestCase):

    mk_mdict = TT.MergeableDict.create

    def test_20_update__w_replace(self):
        dic = self.mk_mdict(dict(name="a", a=1, b=dict(b=[1, 2], c="C")))
        upd = self.mk_mdict(dict(a=2, b=dict(b=[3, 4, 5], d="D")))
        ref = TT.MergeableDict(**dic.copy())
        ref['a'] = 2
        ref['b'] = upd['b']
        ref['b']['c'] = dic['b']['c']

        dic.update(upd, TT.MS_REPLACE)
        self.assertTrue(dicts_equal(dic, ref))

    def test_22_update__w_replace__not_a_dict(self):
        dic = TT.MergeableDict()
        ref = TT.MergeableDict(**dic.copy())
        dic.update(1, TT.MS_REPLACE)
        self.assertTrue(dicts_equal(dic, ref))

    def test_24_update__w_None(self):
        dic = self.mk_mdict(dict(name="a", a=1, b=dict(b=[1, 2], c="C")))
        ref = TT.MergeableDict(**dic.copy())
        dic.update(None)
        self.assertTrue(dicts_equal(dic, ref))

    def test_30_update__wo_replace(self):
        dic = self.mk_mdict(dict(a=1, b=dict(b=[1, 2], c="C")))
        upd = self.mk_mdict(dict(name="foo", a=2, b=dict(b=[3, 4, 5], d="D")))
        ref = TT.MergeableDict(**dic.copy())
        ref['name'] = upd['name']

        dic.update(upd, TT.MS_NO_REPLACE)
        self.assertTrue(dicts_equal(dic, ref))

    def test_40_update_w_merge__primitives(self):
        dic = self.mk_mdict(dict(a=1, b="b"))
        upd = self.mk_mdict(dict(a=2, b="B", c=[1, 2, 3]))
        dic2 = TT.MergeableDict(**dic.copy())
        ref = TT.MergeableDict(**dic.copy())
        ref["c"] = upd["c"]

        dic.update_w_merge(upd)
        self.assertTrue(dicts_equal(dic, upd))

        dic2.update_w_merge(upd, keep=True)
        self.assertTrue(dicts_equal(dic2, ref))

    def test_42_update_w_merge__lists(self):
        dic = TT.MergeableDict(a=[1, 2, 3])
        upd = TT.MergeableDict(a=[1, 4, 5])
        upd2 = TT.MergeableDict(a=1)
        dic2 = TT.MergeableDict(**dic.copy())
        ref = TT.MergeableDict(**dic.copy())
        ref["a"] = [1, 2, 3, 4, 5]

        dic.update_w_merge(upd)
        self.assertTrue(dicts_equal(dic, upd))

        dic2.update_w_merge(upd, merge_lists=True)
        self.assertTrue(dicts_equal(dic2, ref))

        dic2.update_w_merge(upd2, merge_lists=True, keep=True)
        self.assertTrue(dicts_equal(dic2, ref))

        dic2.update_w_merge(upd2, merge_lists=True, keep=False)
        self.assertTrue(dicts_equal(dic2, upd2))

    def test_48_update_w_merge_dicts__complex_case(self):
        dic = self.mk_mdict(dict(name="a", a=1, b=dict(b=[1, 2], c="C"),
                                 e=[3, 4]))
        upd = self.mk_mdict(dict(a=2, b=dict(b=[1, 2, 3], d="D")))
        ref = TT.MergeableDict(**dic.copy())
        ref['a'] = 2
        ref['b'] = TT.MergeableDict(b=[1, 2, 3], c="C", d="D")
        ref['e'] = [3, 4]

        dic.update_w_merge(upd)
        self.assertTrue(dicts_equal(dic, ref))

    def test_50_update__w_merge_dicts_and_lists(self):
        dic = self.mk_mdict(dict(name="a", a=1, b=dict(b=[1, 2], c="C")))
        upd = self.mk_mdict(dict(a=2, b=dict(b=[3, 4], d="D", e=[1, 2])))

        ref = TT.MergeableDict(**dic.copy())
        ref['a'] = 2
        ref['b'] = TT.MergeableDict(b=[1, 2, 3, 4], c="C", d="D", e=[1, 2])

        dic.update(upd, TT.MS_DICTS_AND_LISTS)
        self.assertTrue(dicts_equal(dic, ref))

# vim:sw=4:ts=4:et:
