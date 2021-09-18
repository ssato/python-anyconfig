#
# Copyright (C) 2018 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name
import unittest

import anyconfig.ioinfo
import anyconfig.processors.utils as TT

from anyconfig.common import (
    UnknownFileTypeError, UnknownProcessorTypeError
)
from .common import A, A2, A3, B, C, PRS


PRS = [p() for p in PRS]  # Instantiate all.


class TestCase(unittest.TestCase):

    def test_select_by_key(self):
        ies = (([], []),
               (((['a'], 1), ), [('a', [1])]),
               (((['a', 'aaa'], 1),
                 (['b', 'bb'], 2),
                 (['a'], 3)),
                [('a', [1, 3]),
                 ('aaa', [1]),
                 ('b', [2]),
                 ('bb', [2])]))

        for inp, exp in ies:
            self.assertEqual(TT.select_by_key(inp), exp)

    def test_select_by_key_reversed(self):
        ies = ((((['a', 'aaa'], 1),
                 (['a'], 3)),
                [('a', [3, 1]),
                 ('aaa', [1])]),
               )

        def sfn(itr):
            return sorted(itr, reverse=True)

        for inp, exp in ies:
            self.assertEqual(TT.select_by_key(inp, sfn), exp)

    def test_list_by_x(self):
        (a, a2, a3, b, c) = (A(), A2(), A3(), B(), C())
        ies = ((([], 'type'), []),
               (([a], 'type'), [(a.type(), [a])]),
               (([a], 'extensions'),
                [(x, [a]) for x in a.extensions()]),
               (((a, a2, a3), 'type'),
                [(a.type(), [a3, a2, a])]),
               (([a, b, c], 'type'),
                [(a.type(), [a]), (b.type(), [b, c])]),
               ((PRS, 'type'),
                [(a.type(), [a3, a2, a]), (b.type(), [b, c])]),
               ((PRS, 'extensions'),
                [('js', [a3, a2, a]), ('json', [a3, a2, a]),
                 ('jsn', [a3, a2, a]), ('yaml', [b, c]), ('yml', [b, c])]),
               )

        for prs_key, exp in ies:
            self.assertEqual(
                sorted(TT.list_by_x(*prs_key)), sorted(exp)
            )

    def test_list_by_x_ng_cases(self):
        with self.assertRaises(ValueError):
            TT.list_by_x(PRS, 'undef')

    def test_findall_with_pred__type(self):
        def _findall_by_type(typ):
            return TT.findall_with_pred(lambda p: p.type() == typ, PRS)

        (a, a2, a3, b, c) = (A(), A2(), A3(), B(), C())
        ies = (('json', [a3, a2, a]),
               ('yaml', [b, c]),
               ('undefined', []),
               )

        for inp, exp in ies:
            self.assertEqual(_findall_by_type(inp), exp)

    def test_findall_with_pred__ext(self):
        def _findall_with_pred__ext(ext):
            return TT.findall_with_pred(lambda p: ext in p.extensions(), PRS)

        (a, a2, a3, b, c) = (A(), A2(), A3(), B(), C())
        ies = (('js', [a3, a2, a]),
               ('yml', [b, c]),
               ('xyz', []),
               )

        for inp, exp in ies:
            self.assertEqual(_findall_with_pred__ext(inp), exp)

    def assertInstance(self, obj, cls):
        self.assertTrue(isinstance(obj, cls))

    def test_maybe_processor(self):
        a3 = A3()
        ies = (((a3, A3), True),
               ((A3, A3), True),
               ((B, A3), False),
               )
        for inp, exp in ies:
            afn = self.assertTrue if exp else self.assertFalse
            res = TT.maybe_processor(*inp)
            afn(isinstance(res, A3))

            if not exp:
                self.assertTrue(res is None)

    def test_find_by_type_or_id(self):
        (a, a2, a3, b, c) = (A(), A2(), A3(), B(), C())
        ies = ((('json', PRS), [a3, a2, a]),
               (('yaml', PRS), [b, c]),
               (('dummy', PRS), [c]),
               )
        for inp, exp in ies:
            self.assertEqual(TT.find_by_type_or_id(*inp), exp)

    def test_find_by_type_or_id_ng_cases(self):
        with self.assertRaises(UnknownProcessorTypeError):
            TT.find_by_type_or_id('xyz', PRS)

    def test_find_by_fileext(self):
        ies = ((('js', PRS), [A3(), A2(), A()]),
               (('yml', PRS), [B(), C()]),
               )
        for inp, exp in ies:
            self.assertEqual(TT.find_by_fileext(*inp), exp)

    def test_find_by_fileext_ng_cases(self):
        with self.assertRaises(UnknownFileTypeError):
            TT.find_by_fileext('xyz', PRS)

    def test_find_by_maybe_file(self):
        (a, a2, a3, b, c) = (A(), A2(), A3(), B(), C())
        obj = anyconfig.ioinfo.make('/path/to/a.json')

        ies = ((('/path/to/a.jsn', PRS), [a3, a2, a]),
               (('../../path/to/b.yml', PRS), [b, c]),
               ((obj, PRS), [a3, a2, a]),
               )

        for inp, exp in ies:
            self.assertEqual(TT.find_by_maybe_file(*inp), exp)

    def test_find_by_maybe_file_ng_cases(self):
        ies = (('/tmp/x.xyz', PRS),
               ('/dev/null', PRS),
               )
        for inp in ies:
            with self.assertRaises(UnknownFileTypeError):
                TT.find_by_maybe_file(*inp)

    def test_findall_ng_cases(self):
        ies = (
               ((None, PRS, None), ValueError),  # w/o path nor type
               (('/tmp/x.xyz', PRS, None), UnknownFileTypeError),
               (('/dev/null', PRS, None), UnknownFileTypeError),
               ((None, PRS, 'xyz'), UnknownProcessorTypeError),
               )
        for inp, exc in ies:
            with self.assertRaises(exc):
                TT.findall(*inp)

    def test_findall_by_maybe_file(self):
        (a, a2, a3, b, c) = (A(), A2(), A3(), B(), C())
        obj = anyconfig.ioinfo.make('/path/to/a.json')

        ies = ((('/path/to/a.jsn', PRS), [a3, a2, a]),
               (('../../path/to/b.yml', PRS), [b, c]),
               ((obj, PRS), [a3, a2, a]),
               )
        for inp, exp in ies:
            self.assertEqual(TT.findall(*inp), exp)

    def test_findall_by_type_or_id(self):
        (a, a2, a3, b, c) = (A(), A2(), A3(), B(), C())
        ies = (((None, PRS, 'json'), [a3, a2, a]),
               ((None, PRS, 'yaml'), [b, c]),
               ((None, PRS, 'dummy'), [c]),
               )
        for inp, exp in ies:
            self.assertEqual(TT.findall(*inp), exp)

    def test_find_by_forced_type(self):
        a2 = A2()
        c = C()
        ies = (((None, PRS, A2), a2),
               ((None, PRS, A2), a2),
               ((None, PRS, c.cid()), c),
               )

        for inp, exp in ies:
            self.assertEqual(TT.find(*inp), exp)

    def test_find__maybe_file(self):
        (a3, b) = (A3(), B())
        obj = anyconfig.ioinfo.make('/path/to/a.json')

        ies = ((('/path/to/a.jsn', PRS), a3),
               (('../../path/to/b.yml', PRS), b),
               ((obj, PRS), a3),
               )
        for inp, exp in ies:
            self.assertEqual(TT.find(*inp), exp)

    def test_find__type_or_id(self):
        ies = (((None, PRS, 'json'), A3()),
               ((None, PRS, 'yaml'), B()),
               ((None, PRS, 'dummy'), C()),
               )
        for inp, exp in ies:
            self.assertEqual(TT.find(*inp), exp)

# vim:sw=4:ts=4:et:
