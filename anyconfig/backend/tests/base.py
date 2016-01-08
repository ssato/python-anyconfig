#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, protected-access, invalid-name
from __future__ import absolute_import

import os
import os.path
import unittest

import anyconfig.backend.base as TT  # stands for test target
import anyconfig.tests.common


MZERO = TT.to_container_fn()()


class Test00(unittest.TestCase):

    def setUp(self):
        self.psr = TT.Parser()

    def test_10_type(self):
        self.assertEqual(self.psr.type(), TT.Parser._type)

    def test_20_loads__null_content(self):
        cnf = self.psr.loads('')
        self.assertEqual(cnf, MZERO)
        self.assertTrue(isinstance(cnf, type(MZERO)))

    def test_30_load__ignore_missing(self):
        cpath = os.path.join(os.curdir, "conf_file_should_not_exist")
        assert not os.path.exists(cpath)

        cnf = self.psr.load(cpath, ignore_missing=True)
        self.assertEqual(cnf, MZERO)
        self.assertTrue(isinstance(cnf, type(MZERO)))


class Test10(unittest.TestCase):

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_ensure_outdir_exists(self):
        TT.LOGGER.setLevel(TT.logging.WARN)  # suppress info/debug log msgs.
        outdir = os.path.join(self.workdir, "outdir")
        outfile = os.path.join(outdir, "a.txt")
        TT.ensure_outdir_exists(outfile)

        self.assertTrue(os.path.exists(outdir))

    def test_12_ensure_outdir_exists__no_dir(self):
        TT.ensure_outdir_exists("a.txt")
        self.assertFalse(os.path.exists(os.path.dirname("a.txt")))

# vim:sw=4:ts=4:et:
