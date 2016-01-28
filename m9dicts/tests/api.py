#
# Copyright (C) 2011 - 2016 Satoru SATOH <ssato @ redhat.com>
#
# pylint: disable=missing-docstring,invalid-name
from __future__ import absolute_import

import collections
import unittest
import m9dicts.api as TT
import m9dicts.dicts as MD
import m9dicts.globals as MG

from m9dicts.tests.common import dicts_equal
from m9dicts.compat import OrderedDict


class Test_10_get(unittest.TestCase):

    def test_10_empty_path(self):
        dic = dict(a=1, b=[1, 2])
        (dic2, err) = TT.get(dic, '')
        self.assertEqual(err, '')
        self.assertTrue(dicts_equal(dic2, dic))

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

        self.assertTrue(dicts_equal(TT.get(dic, "")[0], dic))
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


_CNF_0 = OrderedDict((("name", "a"), ("a", 1),
                      ("b", OrderedDict((("b", (1, 2)), ))),
                      ("c", "C"), ("e", [3, 4]), ("f", None)))


class Test_20_make(unittest.TestCase):

    def test_00_null(self):
        md0 = TT.make()

        # check if md0 is an object of base and default class:
        self.assertTrue(isinstance(md0, MD.UpdateWithReplaceDict))
        self.assertTrue(isinstance(md0, MD.UpdateWithMergeDict))
        self.assertTrue(not md0)

    def test_10_default(self):
        md0 = TT.make(_CNF_0)

        self.assertTrue(isinstance(md0, MD.UpdateWithReplaceDict))
        self.assertTrue(isinstance(md0, MD.UpdateWithMergeDict))
        self.assertTrue(isinstance(md0["b"], MD.UpdateWithReplaceDict))
        self.assertTrue(isinstance(md0["b"], MD.UpdateWithMergeDict))
        for k in "name a c e f".split():
            self.assertTrue(md0[k] == _CNF_0[k],
                            "%r vs. %r" % (md0[k], _CNF_0[k]))

    def test_20_merge(self):
        md1 = TT.make(_CNF_0, merge=MG.MS_REPLACE)
        md2 = TT.make(_CNF_0, merge=MG.MS_NO_REPLACE)
        md3 = TT.make(_CNF_0, merge=MG.MS_DICTS_AND_LISTS)

        self.assertTrue(isinstance(md1, MD.UpdateWithReplaceDict))
        self.assertTrue(isinstance(md2, MD.UpdateWoReplaceDict))
        self.assertTrue(isinstance(md3, MD.UpdateWithMergeListsDict))

        for idx, mdn in enumerate((md1, md2, md3)):
            self.assertTrue(isinstance(mdn["b"], type(mdn)),
                            "#%d %r (%r)" % (idx, mdn["b"], type(mdn["b"])))
            for k in "name a c e f".split():
                self.assertTrue(mdn[k] == _CNF_0[k],
                                "%r vs. %r" % (mdn[k], _CNF_0[k]))

        raised = False
        md4 = None
        try:
            md4 = TT.make(_CNF_0, merge="invalid_merge")
        except ValueError:
            raised = True
        self.assertTrue(raised, "md4 = %r" % type(md4))

    def test_30_ordered(self):
        md0 = TT.make(_CNF_0, ordered=True)

        self.assertTrue(isinstance(md0, MD.UpdateWithReplaceDict))
        self.assertTrue(isinstance(md0, MD.UpdateWithMergeOrderedDict))
        self.assertTrue(isinstance(md0["b"], MD.UpdateWithReplaceDict))
        self.assertTrue(isinstance(md0["b"], MD.UpdateWithMergeOrderedDict))
        for k in "name a c e f".split():
            self.assertTrue(md0[k] == _CNF_0[k],
                            "%r vs. %r" % (md0[k], _CNF_0[k]))

    def test_40_namedtuple(self):
        _point = collections.namedtuple("Point", "x y")
        _triangle = collections.namedtuple("Triangle", "p0 p1 p2")
        obj = _triangle(_point(0, 0), _point(1, 0), _point(0, 1))
        md0 = TT.make(obj)

        self.assertTrue(isinstance(md0, MD.UpdateWithMergeOrderedDict))
        self.assertTrue(isinstance(md0["p0"], MD.UpdateWithMergeOrderedDict))

        for k in "p0 p1 p2".split():
            self.assertEqual(md0[MG.NTPL_CLS_KEY], "Triangle")
            for k2 in "x y".split():
                self.assertEqual(md0[k][MG.NTPL_CLS_KEY], "Point")
                ref = getattr(getattr(obj, k), k2)
                self.assertTrue(md0[k][k2] == ref,
                                "%r vs. %r" % (md0[k][k2], ref))


class Test_30_convert_to(unittest.TestCase):

    def test_00_none(self):
        self.assertTrue(TT.convert_to(None) is None)

    def test_10_iterable(self):
        for inp in ([], [0, 1, 2], (), (0, 1), [0, [1, [2]]]):
            self.assertEqual(TT.convert_to(inp), inp)

    def test_20_mdict(self):
        md0 = TT.make(_CNF_0)
        dic0 = TT.convert_to(md0)

        for k in "name a c e f".split():
            self.assertTrue(dic0[k] == md0[k], "%r vs. %r" % (dic0[k], md0[k]))

        for k in dic0["b"].keys():
            self.assertTrue(dic0["b"][k] == md0["b"][k])

    def test_30_to_namedtuple(self):
        _point = collections.namedtuple("Point", "x y")
        _triangle = collections.namedtuple("Triangle", "p0 p1 p2")
        itpl = _triangle(_point(0, 0), _point(1, 0), _point(0, 1))
        md0 = TT.make(itpl)
        otpl = TT.convert_to(md0, to_namedtuple=True)
        self.assertEqual(otpl, itpl)

# vim:sw=4:ts=4:et:
