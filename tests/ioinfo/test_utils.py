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

import anyconfig.ioinfo.utils as TT


class TestCase(unittest.TestCase):

    def test_get_path_and_ext(self):
        this = pathlib.Path(__file__)
        ies = (
            (this, (this.resolve(), 'py')),
        )
        for inp, exp in ies:
            res = TT.get_path_and_ext(inp)
            self.assertEqual(res, exp)

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

                res_2 = sorted(TT.expand_from_path_2(inp))
                self.assertEqual(res_2, sorted(exp), f'{inp!r} vs. {exp!r}')

# vim:sw=4:ts=4:et:
