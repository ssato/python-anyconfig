#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
import pathlib
import unittest

import anyconfig.backend.base.utils as TT
import tests.common


class Test10(unittest.TestCase):

    def setUp(self):
        self.workdir = tests.common.setup_workdir()

    def tearDown(self):
        tests.common.cleanup_workdir(self.workdir)

    def test_10_ensure_outdir_exists(self):
        outdir = pathlib.Path(self.workdir) / "outdir"
        outfile = str(outdir / "a.txt")

        TT.ensure_outdir_exists(outfile)
        self.assertTrue(outdir.exists())

    def test_12_ensure_outdir_exists__no_dir(self):
        workdir = pathlib.Path(self.workdir)
        outpath = workdir / "a.txt"

        TT.ensure_outdir_exists(str(outpath))
        self.assertTrue(workdir.exists())

# vim:sw=4:ts=4:et:
