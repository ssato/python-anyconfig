#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Test cases for anyconfig.utils.files.
"""
import pathlib
import unittest

import anyconfig.api.utils as TT

from anyconfig.ioinfo import make as ioinfo_make


class TestCase(unittest.TestCase):

    def test_are_same_file_types(self):
        fun = TT.are_same_file_types
        this_py = pathlib.Path(__file__)
        this = ioinfo_make(this_py)
        other = ioinfo_make(this_py.parent / 'setup.cfg')

        for inp, exp in (([], False),
                         ([this], True),
                         ([this, this], True),
                         ([this, other], False),
                         ([this, other], False),
                         ):
            (self.assertTrue if exp else self.assertFalse)(fun(inp))

# vim:sw=4:ts=4:et:
