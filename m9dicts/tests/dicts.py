#
# Copyright (C) 2011 - 2016 Satoru SATOH <ssato @ redhat.com>
#
# pylint: disable=missing-docstring,invalid-name
from __future__ import absolute_import
import unittest
import m9dicts.dicts as TT


class Test_10_UpdateWithReplaceDict(unittest.TestCase):

    od0 = TT.OrderedDict((("a", 1), ("b", [1, 3]), ("c", "abc"), ("f", None)))
    up0 = TT.OrderedDict((("a", 2), ("b", [0, 1]),
                          ("c", TT.OrderedDict((("d", "d"), ("e", 1)))),
                          ("d", "d")))
    cls = TT.UpdateWithReplaceDict

    def setUp(self):
        self.mds = (self.cls(self.od0), self.cls(self.od0.items()),
                    self.cls(**self.od0))

    def check_updated(self, *others, **another):
        upd = self.up0
        ref = self.mds[0].copy()

        for md in self.mds:
            md.update(*others, **another)
            self.assertTrue(all(md[k] == upd[k] for k in upd.keys()))
            self.assertTrue(all(md[k] == ref[k] for k in ref.keys()
                                if k not in upd))

    def test_10_update_with_a_mdict(self):
        self.check_updated(self.cls(self.up0))

    def test_12_update_with_a_dict(self):
        self.check_updated(dict(self.up0))

    def test_14_update_with_kv_tuples(self):
        self.check_updated(list(self.up0.items()))

    def test_16_update_with_invalid(self):
        md0 = self.cls(self.od0)
        self.assertTrue(isinstance(md0, self.cls))
        try:
            raised = False
            md0.update(1)
        except (ValueError, TypeError):
            raised = True

        self.assertTrue(raised)

    def test_20_update_with_a_odict_and_kwargs(self):
        other = self.up0.copy()
        another = TT.OrderedDict((("b", other["b"]), ))
        del other["b"]

        self.check_updated(other, **another)


class Test_20_UpdateWoReplaceDict(Test_10_UpdateWithReplaceDict):

    cls = TT.UpdateWoReplaceDict

    def check_updated(self, *others, **another):
        upd = self.up0
        ref = self.mds[0].copy()

        for md in self.mds:
            md.update(*others, **another)
            self.assertTrue(all(md[k] == upd[k] for k in upd.keys()
                                if k not in ref))
            self.assertTrue(all(md[k] == ref[k] for k in ref.keys()))


class Test_30_UpdateWithMergeDict(Test_10_UpdateWithReplaceDict):

    cls = TT.UpdateWithMergeDict
    replaced_keys = "a b d".split()

    def check_updated(self, *others, **another):
        upd = self.up0
        ref = self.mds[0].copy()

        for md in self.mds:
            md.update(*others, **another)
            self.assertTrue(all(md[k] == upd[k] for k in self.replaced_keys))
            self.assertTrue(all(md["c"][k] == upd["c"][k] for k
                                in upd["c"].keys()))
            self.assertTrue(all(md[k] == ref[k] for k in ref.keys()
                                if k not in upd))


class Test_32_UpdateWithMergeDict_kept(Test_10_UpdateWithReplaceDict):

    class UWMDK(TT.UpdateWithMergeDict):
        keep = True

    cls = UWMDK

    def check_updated(self, *others, **another):
        upd = self.up0
        ref = self.mds[0].copy()

        for md in self.mds:
            md.update(*others, **another)
            self.assertTrue(all(md[k] == upd[k] for k in ["d"]))
            self.assertEqual(md["c"], ref["c"])
            self.assertTrue(all(md[k] == ref[k] for k in ref.keys()
                                if k not in upd))


class Test_34_UpdateWithMergeListsDict(Test_30_UpdateWithMergeDict):

    cls = TT.UpdateWithMergeListsDict
    replaced_keys = "a d".split()

    def check_updated(self, *others, **another):
        tcls = Test_34_UpdateWithMergeListsDict
        super(tcls, self).check_updated(*others, **another)
        for md in self.mds:
            self.assertEqual(md["b"], [1, 3, 0])


class Test_40_UpdateWithReplaceOrderedDict(Test_10_UpdateWithReplaceDict):

    cls = TT.UpdateWithReplaceOrderedDict

    def setUp(self):
        self.mds = (self.cls(self.od0), self.cls(self.od0.items()))

    def check_updated(self, *others, **another):
        tcls = Test_40_UpdateWithReplaceOrderedDict
        super(tcls, self).check_updated(*others, **another)
        for md in self.mds:
            self.assertEqual(list(md.keys()), "a b c f d".split())


class Test_50_UpdateWoReplaceOrderedDict(Test_20_UpdateWoReplaceDict):

    cls = TT.UpdateWoReplaceOrderedDict

    def setUp(self):
        self.mds = (self.cls(self.od0), self.cls(self.od0.items()))

    def check_updated(self, *others, **another):
        tcls = Test_50_UpdateWoReplaceOrderedDict
        super(tcls, self).check_updated(*others, **another)
        for md in self.mds:
            self.assertEqual(list(md.keys()), "a b c f d".split())


class Test_60_UpdateWithMergeOrderedDict(Test_30_UpdateWithMergeDict):

    cls = TT.UpdateWithMergeOrderedDict

    def setUp(self):
        self.mds = (self.cls(self.od0), self.cls(self.od0.items()))

    def check_updated(self, *others, **another):
        tcls = Test_60_UpdateWithMergeOrderedDict
        super(tcls, self).check_updated(*others, **another)
        for md in self.mds:
            self.assertEqual(list(md.keys()), "a b c f d".split())


_TCLS = Test_34_UpdateWithMergeListsDict


class Test_62_UpdateWithMergeListsOrderedDict(_TCLS):

    cls = TT.UpdateWithMergeListsOrderedDict

    def setUp(self):
        self.mds = (self.cls(self.od0), self.cls(self.od0.items()))

    def check_updated(self, *others, **another):
        tcls = Test_62_UpdateWithMergeListsOrderedDict
        super(tcls, self).check_updated(*others, **another)
        for md in self.mds:
            self.assertEqual(list(md.keys()), "a b c f d".split())

# vim:sw=4:ts=4:et:
