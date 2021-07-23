#
# Copyright (C) 2018 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name
import unittest

import anyconfig.ioinfo as TT

from anyconfig.common import (
    IOI_PATH_STR, IOI_PATH_OBJ, IOI_STREAM,
    UnknownFileTypeError
)

from .constants import TEST_PY


class TestCase(unittest.TestCase):

    def test_guess_io_type(self):
        ies = (
            (TEST_PY, IOI_PATH_OBJ),
            (str(TEST_PY), IOI_PATH_STR),
            (TEST_PY.open(), IOI_STREAM),
        )
        for inp, exp in ies:
            self.assertEqual(TT.guess_io_type(inp), exp)

    def test_guess_io_type__failures(self):
        with self.assertRaises(ValueError):
            TT.guess_io_type(0)

    def test_inspect_io_obj(self):
        ies = (
            # (args, exp)
            ((TEST_PY, IOI_PATH_OBJ), (str(TEST_PY), 'py')),
            ((TEST_PY.open(), IOI_STREAM), (str(TEST_PY), 'py')),
        )
        for inp, exp in ies:
            self.assertEqual(TT.inspect_io_obj(*inp), exp)

    def test_inspect_io_obj_failiures(self):
        ies = (
            (None, None),
            (TEST_PY, None),
        )
        for inp in ies:
            with self.assertRaises(UnknownFileTypeError):
                TT.inspect_io_obj(*inp)

# vim:sw=4:ts=4:et:
