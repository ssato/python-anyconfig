#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, protected-access
import os
import os.path
import unittest

import anyconfig.backend.base as TT  # stands for test target
import anyconfig.mergeabledict
import anyconfig.tests.common


class Test00(unittest.TestCase):

    def test_10_set_container(self):
        psr = TT.Parser
        psr.set_container(dict)
        self.assertEquals(psr.container(), dict)
        psr.set_container(anyconfig.mergeabledict.MergeableDict)

    def test_10_type(self):
        self.assertEquals(TT.Parser.type(), TT.Parser._type)

    def test_10_type__force_set(self):
        TT.Parser._type = 1
        self.assertEquals(TT.Parser.type(), 1)

    def test_20__load__ignore_missing(self):
        null_cntnr = TT.Parser.container()()
        cpath = os.path.join(os.curdir, "conf_file_should_not_exist")
        assert not os.path.exists(cpath)

        self.assertEquals(TT.Parser.load(cpath, ignore_missing=True),
                          null_cntnr)

    def test_50_load_impl(self):
        raised = False
        try:
            TT.Parser.load_impl("/file/not/exist")
        except NotImplementedError:
            raised = True

        self.assertTrue(raised)

    def test_50_dumps_impl(self):
        raised = False
        try:
            TT.Parser.dumps_impl({})
        except NotImplementedError:
            raised = True

        self.assertTrue(raised)


class Test10(unittest.TestCase):

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_ensure_outdir_exists(self):
        outdir = os.path.join(self.workdir, "outdir")
        outfile = os.path.join(outdir, "a.txt")

        TT.ensure_outdir_exists(outfile)

        self.assertTrue(os.path.exists(outdir))

# vim:sw=4:ts=4:et:
