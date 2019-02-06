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
    _cid = "A"
    _type = "json"
    _extensions = ['json', 'jsn', 'js']


class A2(A):
    _cid = "A2"
    _priority = 20  # Higher priority than A.


class A3(A):
    _cid = "A3"
    _priority = 99  # Higher priority than A and A2.


class B(anyconfig.models.processor.Processor):
    _cid = "B"
    _type = "yaml"
    _extensions = ['yaml', 'yml']
    _priority = 99  # Higher priority than C.


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


class Test_12_list_functions(unittest.TestCase):

    def test_10_list_by_x(self):
        self.assertRaises(ValueError, TT.list_by_x, PRS, "undef")
        self.assertEqual(TT.list_by_x([], "type"), [])

    def test_20_list_by_type(self):
        exp = sorted([(A.type(), [A3, A2, A]), (B.type(), [B, C])],
                     key=TT.operator.itemgetter(0))
        self.assertEqual(TT.list_by_x(PRS, "type"), exp)

    def test_30_list_by_extensions(self):
        exp = sorted([("js", [A3, A2, A]),
                      ("json", [A3, A2, A]),
                      ("jsn", [A3, A2, A]),
                      ("yaml", [B, C]),
                      ("yml", [B, C])],
                     key=TT.operator.itemgetter(0))
        self.assertEqual(TT.list_by_x(PRS, "extensions"), exp)


class Test_20_findall_functions(unittest.TestCase):

    def test_10_findall_with_pred__type(self):
        def _findall_by_type(typ):
            return TT.findall_with_pred(lambda p: p.type() == typ, PRS)

        self.assertEqual(_findall_by_type("json"), [A3, A2, A])
        self.assertEqual(_findall_by_type("yaml"), [B, C])
        self.assertEqual(_findall_by_type("undefined"), [])

    def test_20_findall_with_pred__ext(self):
        def _findall_with_pred__ext(ext):
            return TT.findall_with_pred(lambda p: ext in p.extensions(), PRS)

        self.assertEqual(_findall_with_pred__ext("js"), [A3, A2, A])
        self.assertEqual(_findall_with_pred__ext("yml"), [B, C])
        self.assertEqual(_findall_with_pred__ext("xyz"), [])


class Test_30_find_functions(unittest.TestCase):

    def assertInstance(self, obj, cls):
        self.assertTrue(isinstance(obj, cls))

    def test_16_maybe_processor(self):
        self.assertTrue(isinstance(TT.maybe_processor(A3, A3), A3))
        self.assertTrue(isinstance(TT.maybe_processor(A3(), A3), A3))
        self.assertTrue(TT.maybe_processor("undef", A3) is None)

    def test_20_find_by_type_or_id(self):
        self.assertEqual(TT.find_by_type_or_id("json", PRS), [A3, A2, A])
        self.assertEqual(TT.find_by_type_or_id("yaml", PRS), [B, C])
        self.assertEqual(TT.find_by_type_or_id("dummy", PRS), [C])

    def test_22_find_by_type_or_id__ng_cases(self):
        self.assertRaises(UnknownProcessorTypeError,
                          TT.find_by_type_or_id, "xyz", PRS)

    def test_30_find_by_fileext(self):
        self.assertEqual(TT.find_by_fileext("jsn", PRS), [A3, A2, A])
        self.assertEqual(TT.find_by_fileext("yml", PRS), [B, C])

    def test_32_find_by_fileext__ng_cases(self):
        self.assertRaises(UnknownFileTypeError, TT.find_by_fileext, "xyz", PRS)

    def test_40_find_by_maybe_file(self):
        self.assertEqual(TT.find_by_maybe_file("/path/to/a.jsn", PRS),
                         [A3, A2, A])
        self.assertEqual(TT.find_by_maybe_file("../../path/to/b.yml", PRS),
                         [B, C])
        obj = anyconfig.ioinfo.make("/path/to/a.json")
        self.assertEqual(TT.find_by_maybe_file(obj, PRS), [A3, A2, A])

    def test_42_find_by_maybe_file__ng_cases(self):
        self.assertRaises(UnknownFileTypeError, TT.find_by_maybe_file,
                          "/tmp/x.xyz", PRS)
        self.assertRaises(UnknownFileTypeError, TT.find_by_maybe_file,
                          "/dev/null", PRS)


class Test_32_find_functions(unittest.TestCase):

    def test_10_findall__wo_path_nor_type(self):
        self.assertRaises(ValueError, TT.findall, None, PRS, None)

    def test_12_findall__uknown_file_type(self):
        self.assertRaises(UnknownFileTypeError, TT.findall, "/tmp/x.xyz", PRS)
        self.assertRaises(UnknownFileTypeError, TT.findall, "/dev/null", PRS)

    def test_14_findall__uknown_type(self):
        self.assertRaises(UnknownProcessorTypeError,
                          TT.findall, None, PRS, "xyz")

    def test_20_find__maybe_file(self):
        self.assertEqual(TT.findall("/path/to/a.jsn", PRS), [A3, A2, A])
        self.assertEqual(TT.findall("../../path/to/b.yml", PRS), [B, C])

        obj = anyconfig.ioinfo.make("/path/to/a.json")
        self.assertEqual(TT.findall(obj, PRS), [A3, A2, A])

    def test_22_findall__type_or_id(self):
        self.assertEqual(TT.findall(None, PRS, forced_type="json"),
                         [A3, A2, A])
        self.assertEqual(TT.findall(None, PRS, forced_type="yaml"), [B, C])
        self.assertEqual(TT.findall(None, PRS, "dummy"), [C])

    def test_30_find__forced_type(self):
        self.assertEqual(TT.find(None, PRS, forced_type=A2), A2)
        self.assertEqual(TT.find(None, PRS, forced_type=A2()), A2)
        self.assertEqual(TT.find(None, PRS, forced_type=C.cid()), C)

    def test_32_find__maybe_file(self):
        self.assertEqual(TT.find("/path/to/a.jsn", PRS), A3)
        self.assertEqual(TT.find("../../path/to/b.yml", PRS), B)

        obj = anyconfig.ioinfo.make("/path/to/a.json")
        self.assertEqual(TT.find(obj, PRS), A3)

    def test_34_find__type_or_id(self):
        self.assertEqual(TT.find(None, PRS, forced_type="json"), A3)
        self.assertEqual(TT.find(None, PRS, forced_type="yaml"), B)
        self.assertEqual(TT.find(None, PRS, forced_type="dummy"), C)


class Test_40_Processors(unittest.TestCase):

    def test_10_init(self):
        prcs = TT.Processors()
        self.assertFalse(prcs.list())

    def test_12_init_with_processors(self):
        prcs = TT.Processors(PRS)
        self.assertEqual(prcs.list(sort=True),
                         sorted(PRS, key=operator.methodcaller("cid")))

    def test_20_list_by_cid(self):
        prcs = TT.Processors(PRS)
        exp = sorted(((p.cid(), [p]) for p in PRS),
                     key=TT.operator.itemgetter(0))
        self.assertEqual(prcs.list_by_cid(), exp)

    def test_20_list_x(self):
        prcs = TT.Processors(PRS)
        self.assertRaises(ValueError, prcs.list_x)
        self.assertEqual(prcs.list_x("cid"),
                         sorted(set(p.cid() for p in PRS)))
        self.assertEqual(prcs.list_x("type"),
                         sorted(set(p.type() for p in PRS)))

        res = sorted(set(A.extensions() + B.extensions() + C.extensions()))
        self.assertEqual(prcs.list_x("extension"), res)

# vim:sw=4:ts=4:et:
