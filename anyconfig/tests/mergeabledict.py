#
# Copyright (C) 2011, 2012 Satoru SATOH <satoru.satoh @ gmail.com>
#
import anyconfig.mergeabledict as T
import anyconfig.tests.common as C

import os.path
import unittest


class Test_MergeableDict(unittest.TestCase):

    def test_create(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"), e=[3, 4])
        b = T.MergeableDict.create(a)

        self.assertTrue(isinstance(b, T.MergeableDict))

    def test_update__w_merge_dicts(self):
        a = T.MergeableDict(name="a", a=1,
                            b=T.MergeableDict(b=[1, 2], c="C"),
                            e=[3, 4])
        b = T.MergeableDict(a=2, b=T.MergeableDict(b=[1, 2, 3], d="D"))

        ref = T.MergeableDict(**a.copy())
        ref['a'] = 2
        ref['b'] = T.MergeableDict(b=[1, 2, 3], c="C", d="D")
        ref['e'] = [3, 4]

        a.update(b)

        self.assertEquals(a, ref)

    def test_update__w_merge_dicts_and_lists(self):
        a = T.MergeableDict(name="a", a=1, b=T.MergeableDict(b=[1, 2], c="C"))
        b = T.MergeableDict(a=2, b=T.MergeableDict(b=[3, 4, 5], d="D"))

        ref = T.MergeableDict(**a.copy())
        ref['a'] = 2
        ref['b'] = T.MergeableDict(b=[1, 2, 3, 4, 5], c="C", d="D")

        a.update(b, T.ST_MERGE_DICTS_AND_LISTS)

        self.assertEquals(a, ref)

    def test_update__w_replace(self):
        a = T.MergeableDict(name="a", a=1, b=T.MergeableDict(b=[1, 2], c="C"))
        b = T.MergeableDict(a=2, b=T.MergeableDict(b=[3, 4, 5], d="D"))

        ref = T.MergeableDict(**a.copy())
        ref['a'] = 2
        ref['b'] = b['b']
        ref['b']['c'] = a['b']['c']

        a.update(b, T.ST_REPLACE)

        self.assertEquals(a, ref)

    def test_update__w_None(self):
        a = T.MergeableDict(name="a", a=1, b=T.MergeableDict(b=[1, 2], c="C"))
        ref = T.MergeableDict(**a.copy())

        a.update(None)

        self.assertEquals(a, ref)

# vim:sw=4:ts=4:et:
