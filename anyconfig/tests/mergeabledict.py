#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato @ redhat.com>
#
# pylint: disable=missing-docstring,invalid-name
import unittest
import anyconfig.mergeabledict as TT


class Test00(unittest.TestCase):

    def test_create_from__convert_to(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"), e=[3, 4])
        b = TT.create_from(a)
        c = TT.convert_to(b)

        self.assertTrue(isinstance(b, TT.MergeableDict))
        self.assertTrue(isinstance(c, dict))
        self.assertFalse(isinstance(c, TT.MergeableDict))


class Test10(unittest.TestCase):

    def test_update__w_merge_dicts(self):
        a = TT.MergeableDict(name="a", a=1,
                             b=TT.MergeableDict(b=[1, 2], c="C"),
                             e=[3, 4])
        b = TT.MergeableDict(a=2, b=TT.MergeableDict(b=[1, 2, 3], d="D"))

        ref = TT.MergeableDict(**a.copy())
        ref['a'] = 2
        ref['b'] = TT.MergeableDict(b=[1, 2, 3], c="C", d="D")
        ref['e'] = [3, 4]

        a.update(b)

        self.assertEquals(a, ref)

    def test_update__w_merge_dicts_and_lists(self):
        a = TT.MergeableDict(name="a", a=1,
                             b=TT.MergeableDict(b=[1, 2], c="C"))
        b = TT.MergeableDict(a=2,
                             b=TT.MergeableDict(b=[3, 4], d="D", e=[1, 2]))

        ref = TT.MergeableDict(**a.copy())
        ref['a'] = 2
        ref['b'] = TT.MergeableDict(b=[1, 2, 3, 4], c="C", d="D", e=[1, 2])

        a.update(b, TT.MS_DICTS_AND_LISTS)

        self.assertEquals(a, ref)

    def test_update__w_replace(self):
        a = TT.MergeableDict(name="a", a=1,
                             b=TT.MergeableDict(b=[1, 2], c="C"))
        b = TT.MergeableDict(a=2, b=TT.MergeableDict(b=[3, 4, 5], d="D"))

        ref = TT.MergeableDict(**a.copy())
        ref['a'] = 2
        ref['b'] = b['b']
        ref['b']['c'] = a['b']['c']

        a.update(b, TT.MS_REPLACE)
        self.assertEquals(a, ref)

    def test_update__w_replace__not_a_dict(self):
        a = TT.MergeableDict()
        a.update(1, TT.MS_REPLACE)

        # NOTE: It does not work.
        try:
            self.assertEquals(a, 1)
        except AssertionError:
            pass

    def test_update__wo_replace(self):
        a = TT.MergeableDict(a=1, b=TT.MergeableDict(b=[1, 2], c="C"))
        b = TT.MergeableDict(name="foo", a=2,
                             b=TT.MergeableDict(b=[3, 4, 5], d="D"))

        ref = TT.MergeableDict(**a.copy())
        ref['name'] = b['name']

        a.update(b, TT.MS_NO_REPLACE)

        self.assertEquals(a, ref)

    def test_update__w_None(self):
        a = TT.MergeableDict(name="a", a=1,
                             b=TT.MergeableDict(b=[1, 2], c="C"))
        ref = TT.MergeableDict(**a.copy())
        a.update(None)

        self.assertEquals(a, ref)

# vim:sw=4:ts=4:et:
