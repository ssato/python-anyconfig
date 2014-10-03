#
# Copyright (C) 2011 - 2013 Satoru SATOH <ssato @ redhat.com>
#
import anyconfig.mergeabledict as T
import unittest


class Test_00_utility_functions(unittest.TestCase):

    def test_create_from__convert_to(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"), e=[3, 4])
        b = T.create_from(a)
        c = T.convert_to(b)

        self.assertTrue(isinstance(b, T.MergeableDict))
        self.assertTrue(isinstance(c, dict))
        self.assertFalse(isinstance(c, T.MergeableDict))


class Test_10_MergeableDict(unittest.TestCase):

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
        b = T.MergeableDict(a=2, b=T.MergeableDict(b=[3, 4], d="D", e=[1, 2]))

        ref = T.MergeableDict(**a.copy())
        ref['a'] = 2
        ref['b'] = T.MergeableDict(b=[1, 2, 3, 4], c="C", d="D", e=[1, 2])

        a.update(b, T.MS_DICTS_AND_LISTS)

        self.assertEquals(a, ref)

    def test_update__w_replace(self):
        a = T.MergeableDict(name="a", a=1, b=T.MergeableDict(b=[1, 2], c="C"))
        b = T.MergeableDict(a=2, b=T.MergeableDict(b=[3, 4, 5], d="D"))

        ref = T.MergeableDict(**a.copy())
        ref['a'] = 2
        ref['b'] = b['b']
        ref['b']['c'] = a['b']['c']

        a.update(b, T.MS_REPLACE)
        self.assertEquals(a, ref)

    def test_update__w_replace__not_a_dict(self):
        a = T.MergeableDict()
        a.update(1, T.MS_REPLACE)

        # FIXME: It does not work.
        # self.assertEquals(a, 1)

    def test_update__wo_replace(self):
        a = T.MergeableDict(a=1, b=T.MergeableDict(b=[1, 2], c="C"))
        b = T.MergeableDict(name="foo", a=2,
                            b=T.MergeableDict(b=[3, 4, 5], d="D"))

        ref = T.MergeableDict(**a.copy())
        ref['name'] = b['name']

        a.update(b, T.MS_NO_REPLACE)

        self.assertEquals(a, ref)

    def test_update__w_None(self):
        a = T.MergeableDict(name="a", a=1, b=T.MergeableDict(b=[1, 2], c="C"))
        ref = T.MergeableDict(**a.copy())

        a.update(None)

        self.assertEquals(a, ref)

# vim:sw=4:ts=4:et:
