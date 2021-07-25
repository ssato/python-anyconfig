#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Test cases for anyconfig.utils.files.
"""
import pathlib
import unittest

import anyconfig.ioinfo.utils as TT


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

# vim:sw=4:ts=4:et:
