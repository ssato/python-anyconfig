#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Test cases for anyconfig.utils.files.
"""
import pathlib
import unittest

import anyconfig.utils.files as TT


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

# vim:sw=4:ts=4:et:
