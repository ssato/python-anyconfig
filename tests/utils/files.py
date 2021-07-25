#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Test cases for anyconfig.utils.files.
"""
import pathlib
import tempfile
import unittest

import anyconfig.utils.files as TT

from anyconfig.ioinfo import make as ioinfo_make


class TestCase(unittest.TestCase):

    def test_is_io_stream(self):
        ies = (
            (open(__file__), True),
            (__file__, False),
            ([__file__], False),
            (pathlib.Path(__file__), False),
            ([pathlib.Path(__file__)], False),
        )
        for inp, exp in ies:
            res = TT.is_io_stream(inp)
            (self.assertTrue if exp else self.assertFalse)(res)

    def test_get_path_from_stream(self):
        this = __file__

        with pathlib.Path(this).open() as strm:
            self.assertEqual(TT.get_path_from_stream(strm), this)

        with self.assertRaises(ValueError):
            TT.get_path_from_stream(this)

        self.assertEqual(TT.get_path_from_stream(this, safe=True), '')

    def test_split_path_by_marker(self):
        ies = (
            ('a.txt', ('a.txt', '')),
            ('*.txt', ('', '*.txt')),
            ('a/*.txt', ('a', '*.txt')),
            ('a/b/*.txt', ('a/b', '*.txt')),
            ('a/b/*/*.txt', ('a/b', '*/*.txt')),
        )
        for inp, exp in ies:
            self.assertEqual(TT.split_path_by_marker(inp), exp)

    def test_expand_paths(self):
        with tempfile.TemporaryDirectory() as workdir:
            tdir = pathlib.Path(str(workdir)) / 'a' / 'b' / 'c'
            tdir.mkdir(parents=True)

            pathlib.Path(tdir / 'd.txt').touch()
            pathlib.Path(tdir / 'e.txt').touch()
            pathlib.Path(tdir / 'f.json').write_text("{'a': 1}\n")

            path = tdir / 'd.txt'
            for inp, exp in ((str(path), [path]),
                             (path, [path]),
                             (ioinfo_make(path), [ioinfo_make(path)]),
                             (tdir / '*.txt',
                              [tdir / 'd.txt', tdir / 'e.txt']),
                             (tdir.parent / '**' / '*.txt',
                              [tdir / 'd.txt', tdir / 'e.txt']),
                             (tdir.parent / '**' / '*.*',
                              [tdir / 'd.txt',
                               tdir / 'e.txt',
                               tdir / 'f.json']),
                             ([tdir / 'e.txt', tdir / 'd.txt'],
                              [tdir / 'e.txt', tdir / 'd.txt'])
                             ):
                self.assertEqual(
                    TT.expand_paths(inp), exp, f'{inp!r} vs. {exp!r}'
                )

            with path.open() as fobj:
                self.assertEqual(TT.expand_paths(fobj), [fobj])

# vim:sw=4:ts=4:et:
