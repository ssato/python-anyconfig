#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, protected-access, invalid-name
from __future__ import absolute_import

import os
import pathlib
import unittest

import anyconfig.backend.base as TT  # stands for test target
import anyconfig.ioinfo
import tests.common


MZERO = TT.Parser()._container_factory()()


class Test00(unittest.TestCase):

    def setUp(self):
        self.psr = TT.Parser()

    def test_10_type(self):
        self.assertEqual(self.psr.type(), TT.Parser._type)

    def test_20_loads__null_content(self):
        cnf = self.psr.loads('')
        self.assertEqual(cnf, MZERO)
        self.assertTrue(isinstance(cnf, type(MZERO)))

    def test_30_load__ac_ignore_missing(self):
        cpath = pathlib.Path(os.curdir) / "conf_file_not_exist.json"
        assert not cpath.exists()

        ioi = anyconfig.ioinfo.make(str(cpath))
        cnf = self.psr.load(ioi, ac_ignore_missing=True)
        self.assertEqual(cnf, MZERO)
        self.assertTrue(isinstance(cnf, type(MZERO)))


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


class Test20(unittest.TestCase):

    def test_10_TextFilesMixin_ropen(self):
        with TT.TextFilesMixin.ropen("/dev/null") as fileobj:
            self.assertEqual(fileobj.mode, 'r')

    def test_10_TextFilesMixin_wopen(self):
        with TT.TextFilesMixin.wopen("/dev/null") as fileobj:
            self.assertEqual(fileobj.mode, 'w')

    def test_20_BinaryFilesMixin_ropen(self):
        with TT.BinaryFilesMixin.ropen("/dev/null") as fileobj:
            self.assertEqual(fileobj.mode, 'rb')

    def test_20_BinaryFilesMixin_wopen(self):
        with TT.BinaryFilesMixin.wopen("/dev/null") as fileobj:
            self.assertEqual(fileobj.mode, 'wb')

# vim:sw=4:ts=4:et:
