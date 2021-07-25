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

import anyconfig.ioinfo.paths as TT

from anyconfig.ioinfo import make as ioinfo_make


class TestCase(unittest.TestCase):

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
                exp = [ioinfo_make(e) for e in exp]
                self.assertEqual(
                    TT.expand_paths(inp), exp, f'{inp!r} vs. {exp!r}'
                )

            with path.open() as fobj:
                res = TT.expand_paths(fobj)
                self.assertEqual(res, [ioinfo_make(fobj)])

# vim:sw=4:ts=4:et:
