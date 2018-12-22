#
# Copyright (C) 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
import operator
import unittest
import anyconfig.ioinfo
import anyconfig.models.processor
import anyconfig.processors as TT

from anyconfig.globals import (
    UnknownProcessorTypeError, UnknownFileTypeError
)


class A(anyconfig.models.processor.Processor):
    _type = "json"
    _extensions = ['json', 'jsn', 'js']


class A2(A):
    pass


class A3(A):
    _priority = 99  # Higher priority than A.


class B(anyconfig.models.processor.Processor):
    _type = "yaml"
    _extensions = ['yaml', 'yml']


class C(anyconfig.models.processor.Processor):
    _cid = "dummy"
    _type = "yaml"
    _extensions = ['yaml', 'yml']


PRS = [A, A2, A3, B, C]


class Test_10_Processor(unittest.TestCase):

    def test_10_eq(self):
        (a1, a2, a22, b) = (A(), A(), A2(), B())
        self.assertEqual(a1, a2)
        self.assertNotEqual(a1, b)
        self.assertNotEqual(a1, a22)


class Test_30_find_functions(unittest.TestCase):

    def assertInstance(self, obj, cls):
        self.assertTrue(isinstance(obj, cls))

    def test_10_find_with_pred__type(self):
        self.assertEqual(TT.find_with_pred(lambda p: p.type() == "json", PRS),
                         A3)

        self.assertEqual(TT.find_with_pred(lambda p: p.type() == "yaml", PRS),
                         B)

        self.assertTrue(TT.find_with_pred(lambda p: p.type() == "X",
                                          PRS) is None)

    def test_12_find_with_pred__ext(self):
        p = TT.find_with_pred(lambda p: 'js' in p.extensions(), PRS)
        self.assertEqual(p, A3)

        p = TT.find_with_pred(lambda p: 'yml' in p.extensions(), PRS)
        self.assertEqual(p, B)

        p = TT.find_with_pred(lambda p: 'xyz' in p.extensions(), PRS)
        self.assertTrue(p is None)

    def test_20_find_by_type(self):
        self.assertTrue(isinstance(TT.find_by_type("json", PRS), A3))
        self.assertTrue(isinstance(TT.find_by_type("yaml", PRS), B))
        self.assertRaises(UnknownProcessorTypeError, TT.find_by_type,
                          "X", PRS)

    def test_24_find_by_type_or_id(self):
        self.assertTrue(isinstance(TT.find_by_type_or_id("json", PRS), A3))
        self.assertTrue(isinstance(TT.find_by_type_or_id("yaml", PRS), B))
        self.assertTrue(isinstance(TT.find_by_type_or_id("dummy", PRS), C))

    def test_30_find_by_fileext(self):
        self.assertEqual(TT.find_by_fileext("jsn", PRS), A3)
        self.assertEqual(TT.find_by_fileext("yml", PRS), B)
        self.assertTrue(TT.find_by_fileext("xyz", PRS) is None)

    def test_40_find_by_maybe_file(self):
        self.assertInstance(TT.find_by_maybe_file("/path/to/a.jsn", PRS), A3)
        self.assertInstance(TT.find_by_maybe_file("../../path/to/b.yml", PRS),
                            B)

        obj = anyconfig.ioinfo.make("/path/to/a.json")
        self.assertInstance(TT.find_by_maybe_file(obj, PRS), A3)

    def test_42_find_by_maybe_file__ng_cases(self):
        self.assertRaises(UnknownFileTypeError, TT.find_by_maybe_file,
                          "/tmp/x.xyz", PRS)
        self.assertRaises(UnknownFileTypeError, TT.find_by_maybe_file,
                          "/dev/null", PRS)

    def test_50_find__wo_path_and_type(self):
        self.assertRaises(ValueError, TT.find, None, PRS, None)

    def test_52_find__with_forced_type(self):
        self.assertTrue(isinstance(TT.find(None, PRS, forced_type=A2), A2))
        self.assertTrue(isinstance(TT.find(None, PRS, forced_type=A2()), A2))

    def test_54_find__uknown_file_type(self):
        self.assertRaises(UnknownFileTypeError, TT.find, "/tmp/x.xyz", PRS)
        self.assertRaises(UnknownFileTypeError, TT.find, "/dev/null", PRS)

    def test_56_find__uknown_type(self):
        self.assertRaises(UnknownProcessorTypeError, TT.find, None, PRS, "xyz")


class Test_40_Processors(unittest.TestCase):

    def test_10_init(self):
        prcs = TT.Processors()
        self.assertFalse(prcs.list())

    def test_12_init_with_processors(self):
        prcs = TT.Processors(PRS)
        self.assertEqual(prcs.list(), sorted(PRS,
                                             key=operator.methodcaller("cid")))

# vim:sw=4:ts=4:et:
