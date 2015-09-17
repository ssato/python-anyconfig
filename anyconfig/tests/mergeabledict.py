#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato @ redhat.com>
#
# pylint: disable=missing-docstring,invalid-name
from __future__ import absolute_import

import unittest
import anyconfig.mergeabledict as TT

from anyconfig.tests.common import dicts_equal


class Test00Functions(unittest.TestCase):

    def test_create_from__convert_to(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"), e=[3, 4])
        b = TT.create_from(a)
        c = TT.convert_to(b)

        self.assertTrue(isinstance(b, TT.MergeableDict))
        self.assertTrue(isinstance(c, dict))
        self.assertFalse(isinstance(c, TT.MergeableDict))


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

    def test_40_update__w_merge_dicts(self):
        dic = self.mk_mdict(dict(name="a", a=1, b=dict(b=[1, 2], c="C"),
                                 e=[3, 4]))
        upd = self.mk_mdict(dict(a=2, b=dict(b=[1, 2, 3], d="D")))

        ref = TT.MergeableDict(**dic.copy())
        ref['a'] = 2
        ref['b'] = TT.MergeableDict(b=[1, 2, 3], c="C", d="D")
        ref['e'] = [3, 4]

        dic.update_w_merge(upd)
        self.assertTrue(dicts_equal(dic, ref))

    def test_40_update__w_merge_dicts_and_lists(self):
        dic = self.mk_mdict(dict(name="a", a=1, b=dict(b=[1, 2], c="C")))
        upd = self.mk_mdict(dict(a=2, b=dict(b=[3, 4], d="D", e=[1, 2])))

        ref = TT.MergeableDict(**dic.copy())
        ref['a'] = 2
        ref['b'] = TT.MergeableDict(b=[1, 2, 3, 4], c="C", d="D", e=[1, 2])

        dic.update(upd, TT.MS_DICTS_AND_LISTS)
        self.assertTrue(dicts_equal(dic, ref))

# vim:sw=4:ts=4:et:
