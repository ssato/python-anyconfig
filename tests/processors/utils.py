#
# Copyright (C) 2018 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name
import unittest

import anyconfig.ioinfo
import anyconfig.processors.utils as TT

from anyconfig.common import (
    UnknownProcessorTypeError, UnknownFileTypeError
)

from .common import A, A2, A3, B, C, PRS


class Test_12_list_functions(unittest.TestCase):

    def test_10_list_by_x(self):
        self.assertRaises(ValueError, TT.list_by_x, PRS, 'undef')
        self.assertEqual(TT.list_by_x([], 'type'), [])

    def test_20_list_by_type(self):
        exp = sorted([(A.type(), [A3, A2, A]), (B.type(), [B, C])],
                     key=TT.operator.itemgetter(0))
        self.assertEqual(TT.list_by_x(PRS, 'type'), exp)

    def test_30_list_by_extensions(self):
        exp = sorted([('js', [A3, A2, A]),
                      ('json', [A3, A2, A]),
                      ('jsn', [A3, A2, A]),
                      ('yaml', [B, C]),
                      ('yml', [B, C])],
                     key=TT.operator.itemgetter(0))
        self.assertEqual(TT.list_by_x(PRS, 'extensions'), exp)


class Test_20_findall_functions(unittest.TestCase):

    def test_10_findall_with_pred__type(self):
        def _findall_by_type(typ):
            return TT.findall_with_pred(lambda p: p.type() == typ, PRS)

        self.assertEqual(_findall_by_type('json'), [A3, A2, A])
        self.assertEqual(_findall_by_type('yaml'), [B, C])
        self.assertEqual(_findall_by_type('undefined'), [])

    def test_20_findall_with_pred__ext(self):
        def _findall_with_pred__ext(ext):
            return TT.findall_with_pred(lambda p: ext in p.extensions(), PRS)

        self.assertEqual(_findall_with_pred__ext('js'), [A3, A2, A])
        self.assertEqual(_findall_with_pred__ext('yml'), [B, C])
        self.assertEqual(_findall_with_pred__ext('xyz'), [])


class Test_30_find_functions(unittest.TestCase):

    def assertInstance(self, obj, cls):
        self.assertTrue(isinstance(obj, cls))

    def test_16_maybe_processor(self):
        self.assertTrue(isinstance(TT.maybe_processor(A3, A3), A3))
        self.assertTrue(isinstance(TT.maybe_processor(A3(), A3), A3))
        self.assertTrue(TT.maybe_processor('undef', A3) is None)

    def test_20_find_by_type_or_id(self):
        self.assertEqual(TT.find_by_type_or_id('json', PRS), [A3, A2, A])
        self.assertEqual(TT.find_by_type_or_id('yaml', PRS), [B, C])
        self.assertEqual(TT.find_by_type_or_id('dummy', PRS), [C])

    def test_22_find_by_type_or_id__ng_cases(self):
        self.assertRaises(UnknownProcessorTypeError,
                          TT.find_by_type_or_id, 'xyz', PRS)

    def test_30_find_by_fileext(self):
        self.assertEqual(TT.find_by_fileext('jsn', PRS), [A3, A2, A])
        self.assertEqual(TT.find_by_fileext('yml', PRS), [B, C])

    def test_32_find_by_fileext__ng_cases(self):
        self.assertRaises(UnknownFileTypeError, TT.find_by_fileext, 'xyz', PRS)

    def test_40_find_by_maybe_file(self):
        self.assertEqual(TT.find_by_maybe_file('/path/to/a.jsn', PRS),
                         [A3, A2, A])
        self.assertEqual(TT.find_by_maybe_file('../../path/to/b.yml', PRS),
                         [B, C])
        obj = anyconfig.ioinfo.make('/path/to/a.json')
        self.assertEqual(TT.find_by_maybe_file(obj, PRS), [A3, A2, A])

    def test_42_find_by_maybe_file__ng_cases(self):
        self.assertRaises(UnknownFileTypeError, TT.find_by_maybe_file,
                          '/tmp/x.xyz', PRS)
        self.assertRaises(UnknownFileTypeError, TT.find_by_maybe_file,
                          '/dev/null', PRS)


class Test_32_find_functions(unittest.TestCase):

    def test_10_findall__wo_path_nor_type(self):
        self.assertRaises(ValueError, TT.findall, None, PRS, None)

    def test_12_findall__uknown_file_type(self):
        self.assertRaises(UnknownFileTypeError, TT.findall, '/tmp/x.xyz', PRS)
        self.assertRaises(UnknownFileTypeError, TT.findall, '/dev/null', PRS)

    def test_14_findall__uknown_type(self):
        self.assertRaises(UnknownProcessorTypeError,
                          TT.findall, None, PRS, 'xyz')

    def test_20_find__maybe_file(self):
        self.assertEqual(TT.findall('/path/to/a.jsn', PRS), [A3, A2, A])
        self.assertEqual(TT.findall('../../path/to/b.yml', PRS), [B, C])

        obj = anyconfig.ioinfo.make('/path/to/a.json')
        self.assertEqual(TT.findall(obj, PRS), [A3, A2, A])

    def test_22_findall__type_or_id(self):
        self.assertEqual(TT.findall(None, PRS, forced_type='json'),
                         [A3, A2, A])
        self.assertEqual(TT.findall(None, PRS, forced_type='yaml'), [B, C])
        self.assertEqual(TT.findall(None, PRS, 'dummy'), [C])

    def test_30_find__forced_type(self):
        self.assertEqual(TT.find(None, PRS, forced_type=A2), A2)
        self.assertEqual(TT.find(None, PRS, forced_type=A2()), A2)
        self.assertEqual(TT.find(None, PRS, forced_type=C.cid()), C)

    def test_32_find__maybe_file(self):
        self.assertEqual(TT.find('/path/to/a.jsn', PRS), A3)
        self.assertEqual(TT.find('../../path/to/b.yml', PRS), B)

        obj = anyconfig.ioinfo.make('/path/to/a.json')
        self.assertEqual(TT.find(obj, PRS), A3)

    def test_34_find__type_or_id(self):
        self.assertEqual(TT.find(None, PRS, forced_type='json'), A3)
        self.assertEqual(TT.find(None, PRS, forced_type='yaml'), B)
        self.assertEqual(TT.find(None, PRS, forced_type='dummy'), C)

# vim:sw=4:ts=4:et:
