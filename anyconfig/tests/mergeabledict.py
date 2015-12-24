#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato @ redhat.com>
#
# pylint: disable=missing-docstring,invalid-name
from __future__ import absolute_import

import collections
import unittest
import anyconfig.mergeabledict as TT

from anyconfig.tests.common import dicts_equal


class Test_00_Functions(unittest.TestCase):

    def test_20_get__invalid_inputs(self):
        dic = dict(a=1, b=[1, 2])
        (dic2, err) = TT.get(dic, '')
        self.assertEqual(err, '')
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

    def test_24_get__json_pointer__array(self):
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


_CNF_0 = TT.OrderedDict((("name", "a"), ("a", 1),
                         ("b", TT.OrderedDict((("b", (1, 2)), ))),
                         ("c", "C"), ("e", [3, 4]), ("f", None)))


class Test_30_create_from(unittest.TestCase):

    def test_00_null(self):
        md0 = TT.create_from()

        # check if md0 is an object of base and default class:
        self.assertTrue(isinstance(md0, TT.UpdateWithReplaceDict))
        self.assertTrue(isinstance(md0, TT.UpdateWithMergeDict))
        self.assertTrue(not md0)

    def test_10_default(self):
        md0 = TT.create_from(_CNF_0)

        self.assertTrue(isinstance(md0, TT.UpdateWithReplaceDict))
        self.assertTrue(isinstance(md0, TT.UpdateWithMergeDict))
        self.assertTrue(isinstance(md0["b"], TT.UpdateWithReplaceDict))
        self.assertTrue(isinstance(md0["b"], TT.UpdateWithMergeDict))
        for k in "name a c e f".split():
            self.assertTrue(md0[k] == _CNF_0[k],
                            "%r vs. %r" % (md0[k], _CNF_0[k]))

    def test_20__merge_type(self):
        md1 = TT.create_from(_CNF_0, ac_merge=TT.MS_REPLACE)
        md2 = TT.create_from(_CNF_0, ac_merge=TT.MS_NO_REPLACE)
        md3 = TT.create_from(_CNF_0, ac_merge=TT.MS_DICTS_AND_LISTS)

        self.assertTrue(isinstance(md1, TT.UpdateWithReplaceDict))
        self.assertTrue(isinstance(md2, TT.UpdateWoReplaceDict))
        self.assertTrue(isinstance(md3, TT.UpdateWithMergeListsDict))

        for mdn in (md1, md2, md3):
            self.assertTrue(isinstance(mdn["b"], type(mdn)),
                            "%r (%r)" % (mdn["b"], type(mdn["b"])))
            for k in "name a c e f".split():
                self.assertTrue(mdn[k] == _CNF_0[k],
                                "%r vs. %r" % (mdn[k], _CNF_0[k]))

    def test_30_ordered(self):
        md0 = TT.create_from(_CNF_0, ac_ordered=True)

        self.assertTrue(isinstance(md0, TT.UpdateWithReplaceDict))
        self.assertTrue(isinstance(md0, TT.UpdateWithMergeOrderedDict))
        self.assertTrue(isinstance(md0["b"], TT.UpdateWithReplaceDict))
        self.assertTrue(isinstance(md0["b"], TT.UpdateWithMergeOrderedDict))
        for k in "name a c e f".split():
            self.assertTrue(md0[k] == _CNF_0[k],
                            "%r vs. %r" % (md0[k], _CNF_0[k]))

    def test_40_namedtuple(self):
        _point = collections.namedtuple("Point", "x y")
        _triangle = collections.namedtuple("Triangle", "p0 p1 p2")
        obj = _triangle(_point(0, 0), _point(1, 0), _point(0, 1))
        md0 = TT.create_from(obj)

        self.assertTrue(isinstance(md0, TT.UpdateWithMergeOrderedDict))
        self.assertTrue(isinstance(md0["p0"], TT.UpdateWithMergeOrderedDict))
        for k in "p0 p1 p2".split():
            self.assertEqual(md0[TT.NAMEDTUPLE_CLS_KEY], "Triangle")
            for k2 in "x y".split():
                self.assertEqual(md0[k][TT.NAMEDTUPLE_CLS_KEY], "Point")
                ref = getattr(getattr(obj, k), k2)
                self.assertTrue(md0[k][k2] == ref,
                                "%r vs. %r" % (md0[k][k2], ref))


class Test_40_convert_to(unittest.TestCase):

    def test_00_none(self):
        self.assertTrue(TT.convert_to(None) is None)

    def test_10_iterable(self):
        for inp in ([], [0, 1, 2], (), (0, 1), [0, [1, [2]]]):
            self.assertEqual(TT.convert_to(inp), inp)

    def test_20_mdict(self):
        md0 = TT.create_from(_CNF_0)
        dic0 = TT.convert_to(md0)

        for k in "name a c e f".split():
            self.assertTrue(dic0[k] == md0[k], "%r vs. %r" % (dic0[k], md0[k]))

        for k in dic0["b"].keys():
            self.assertTrue(dic0["b"][k] == md0["b"][k])

    def test_30_to_namedtuple(self):
        _point = collections.namedtuple("Point", "x y")
        _triangle = collections.namedtuple("Triangle", "p0 p1 p2")
        itpl = _triangle(_point(0, 0), _point(1, 0), _point(0, 1))
        md0 = TT.create_from(itpl)
        otpl = TT.convert_to(md0, to_namedtuple=True)
        self.assertEqual(otpl, itpl)

# vim:sw=4:ts=4:et:
