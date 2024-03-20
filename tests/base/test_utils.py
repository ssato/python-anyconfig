#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
import pathlib
import unittest

from . import constants, utils as TT


RES_DIR = constants.RES_DIR / 'base'
SELF = pathlib.Path(__file__)


class TestCase(unittest.TestCase):

    def test_target_by_parent(self):
        aes = [
            ((), 'base'),
            ((__file__, ), 'base'),
        ]
        for args, exp in aes:
            self.assertEqual(TT.target_by_parent(*args), exp)

    def test_load_from_py(self):
        constants_py_path = SELF.parent / 'constants.py'
        aes = [
            ((constants_py_path, ), constants.DATA),
            ((str(constants_py_path), ), constants.DATA),
            ((constants_py_path, 'RES_DIR'), constants.RES_DIR),
        ]
        for args, exp in aes:
            self.assertEqual(
                TT.load_from_py(*args), exp,
                f'args: {args!r}, exp: {exp!r}'
            )

    def test_load_literal_data_from_py(self):
        py_path = RES_DIR / 'basics' / '20' / '00.py'
        exp = TT.json.load(
            (RES_DIR / 'basics' / '10' / '00.json').open()
        )
        aes = [
            (py_path, exp),
            (str(py_path), exp),
        ]
        for arg, exp in aes:
            self.assertEqual(
                TT.load_literal_data_from_py(arg), exp
            )

    def test_maybe_data_path(self):
        aes = [
            ((SELF.parent, SELF.stem, ), SELF),
            ((pathlib.Path('/not/exist/dir'), 'foo', ), None),
        ]
        for args, exp in aes:
            self.assertEqual(TT.maybe_data_path(*args), exp)

    def test_maybe_data_path_failures(self):
        aes = [
            (SELF.parent, SELF.stem, (SELF.parent.name, ), '.xyz'),
        ]
        for args in aes:
            with self.assertRaises(OSError):
                TT.maybe_data_path(*args)

    def test_load_data(self):
        aes = [
            ((None, ), {}),
            ((None, 1), 1),
            ((RES_DIR / 'basics' / '10' / '00.json', ),
             TT.json.load((RES_DIR / 'basics' / '10' / '00.json').open())
             ),
            ((RES_DIR / 'basics' / '20' / '00.py', ),
             TT.json.load((RES_DIR / 'basics' / '10' / '00.json').open())
             ),
            ((RES_DIR / 'basics' / '30' / '20.txt', ),
             (RES_DIR / 'basics' / '10' / '20.json').read_text()
             ),
        ]
        for args, exp in aes:
            res = TT.load_data(*args)
            self.assertEqual(res, exp, res)

    def test_load_data_failures(self):
        aes = [
            (pathlib.Path('not_exist.xyz'), ),
        ]
        for args in aes:
            with self.assertRaises(ValueError):
                TT.load_data(*args)

    def test_load_datasets_from_dir(self):
        aes = [
            ((RES_DIR / 'basics' / '10', '*.json'), 3),
            ((RES_DIR / 'basics' / '20', '*.py'), 1),
            ((RES_DIR / 'basics' / '30', '*.txt'), 3),
        ]
        for args, exp in aes:
            res = TT.load_datasets_from_dir(
                args[0], lambda *xs: xs[1], pattern=args[1]
            )
            self.assertTrue(bool(res))
            self.assertEqual(len(res), exp)

    def test_load_datasets_from_dir_failures(self):
        with self.assertRaises(ValueError):
            _ = TT.load_datasets_from_dir(SELF, list)

# vim:sw=4:ts=4:et:
