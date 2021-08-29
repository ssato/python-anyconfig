#
# Copyright (C) 2018 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name
"""Test cases for anyconfig.ioinfo.factory.
"""
import pathlib
import tempfile
import unittest

import anyconfig.ioinfo.factory as TT

from anyconfig.ioinfo.datatypes import (
    IOInfo, IOI_PATH_OBJ, IOI_STREAM
)

from .constants import TEST_PY


TEST_IOI_PATH_OBJ = IOInfo(
    src=TEST_PY, type=IOI_PATH_OBJ, path=str(TEST_PY), extension='py'
)
TEST_IOI_STREAM = IOInfo(
    src=TEST_PY.open(), type=IOI_STREAM, path=str(TEST_PY), extension='py'
)


class TestCase(unittest.TestCase):

    def test_make(self):
        ies = (
            (TEST_IOI_PATH_OBJ, TEST_IOI_PATH_OBJ),
            (TEST_IOI_STREAM, TEST_IOI_STREAM),
            (str(TEST_PY), TEST_IOI_PATH_OBJ),
        )
        for inp, exp in ies:
            self.assertEqual(TT.make(inp), exp)

    def test_make_failures(self):
        inps = (None, )
        for inp in inps:
            with self.assertRaises(ValueError):
                TT.make(inp)

    def test_expand_from_path(self):
        with tempfile.TemporaryDirectory() as workdir:
            tdir = pathlib.Path(str(workdir)) / 'a' / 'b' / 'c'
            tdir.mkdir(parents=True)

            pathlib.Path(tdir / 'd.txt').touch()
            pathlib.Path(tdir / 'e.txt').touch()
            pathlib.Path(tdir / 'f.json').write_text("{'a': 1}\n")

            path = tdir / 'd.txt'

            for inp, exp in ((path, [path]),
                             (tdir / '*.txt',
                              [tdir / 'd.txt', tdir / 'e.txt']),
                             (tdir.parent / '**' / '*.txt',
                              [tdir / 'd.txt', tdir / 'e.txt']),
                             (tdir.parent / '**' / '*.*',
                              [tdir / 'd.txt',
                               tdir / 'e.txt',
                               tdir / 'f.json']),
                             ):
                res = sorted(TT.expand_from_path(inp))
                self.assertEqual(res, sorted(exp), f'{inp!r} vs. {exp!r}')

# vim:sw=4:ts=4:et:
