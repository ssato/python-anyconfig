#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import os
import os.path
import unittest

import anyconfig.backend.base as TT  # stands for test target
import anyconfig.mergeabledict
import anyconfig.tests.common


class Test_00_ConfigParser(unittest.TestCase):

    def test_10_set_container(self):
        cp = TT.ConfigParser
        cp.set_container(dict)
        self.assertEquals(cp.container(), dict)
        cp.set_container(anyconfig.mergeabledict.MergeableDict)

    def test_10_type(self):
        self.assertEquals(TT.ConfigParser.type(), TT.ConfigParser._type)

    def test_10_type__force_set(self):
        TT.ConfigParser._type = 1
        self.assertEquals(TT.ConfigParser.type(), 1)

    def test_20__load__ignore_missing(self):
        null_cntnr = TT.ConfigParser.container()()
        cpath = os.path.join(os.curdir, "conf_file_should_not_exist")
        assert not os.path.exists(cpath)

        self.assertEquals(TT.ConfigParser.load(cpath, ignore_missing=True),
                          null_cntnr)

    def test_50_load_impl(self):
        raised = False
        try:
            TT.ConfigParser.load_impl("/file/not/exist")
        except NotImplementedError:
            raised = True

        self.assertTrue(raised)

    def test_50_dumps_impl(self):
        raised = False
        try:
            TT.ConfigParser.dumps_impl({})
        except NotImplementedError:
            raised = True

        self.assertTrue(raised)


class Test_10_effectful_functions(unittest.TestCase):

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_mk_dump_dir_if_not_exist(self):
        dumpdir = os.path.join(self.workdir, "dumpdir")
        dumpfile = os.path.join(dumpdir, "a.txt")

        TT.mk_dump_dir_if_not_exist(dumpfile)

        self.assertTrue(os.path.exists(dumpdir))

# vim:sw=4:ts=4:et:
