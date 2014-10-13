#
# Copyright (C) 2012 - 2014 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.base as TT  # stands for test target
import os
import os.path
import unittest


class Test_00_ConfigParser(unittest.TestCase):

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

# vim:sw=4:ts=4:et:
