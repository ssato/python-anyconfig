#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.backend.base.utils.
"""
import pathlib
import tempfile
import unittest

import anyconfig.backend.base.utils as TT


FILENAME = 'file_not_exist.txt'


class TestCase(unittest.TestCase):

    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            TT.not_implemented()

    def test_ensure_outdir_exists_for_file_if_it_exists(self):
        outdir = pathlib.Path.cwd()
        outfile = outdir / FILENAME

        TT.ensure_outdir_exists(outfile)
        TT.ensure_outdir_exists(str(outfile))
        self.assertTrue(outdir.exists())

    def test_ensure_outdir_exists_for_file_if_it_does_not_exist(self):
        with tempfile.TemporaryDirectory() as outdir:
            outdir = pathlib.Path(outdir)
            outpath = outdir / FILENAME

            TT.ensure_outdir_exists(outpath)
            self.assertTrue(outdir.exists())

    def test_ensure_outdir_exists_for_file_if_its_parent_does_not_exist(self):
        with tempfile.TemporaryDirectory() as parent:
            outdir = pathlib.Path(parent) / 'a' / 'b' / 'c'
            outpath = outdir / FILENAME

            TT.ensure_outdir_exists(outpath)
            self.assertTrue(outdir.exists())

# vim:sw=4:ts=4:et:
