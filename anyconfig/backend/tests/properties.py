#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import os.path
import unittest

import anyconfig.backend.properties as TT
import anyconfig.tests.common

from anyconfig.tests.common import dicts_equal


CNF_S = """
a = 0
b = bbb

sect0.c = x;y;z
sect1.d = \\
    1,2,3
"""
CNF = {"a": "0", "b": "bbb", "sect0.c": "x;y;z",
       "sect1.d": "1,2,3"}


class Test(unittest.TestCase):

    def setUp(self):
        self.psr = TT.Parser()
        self.workdir = anyconfig.tests.common.setup_workdir()
        self.cpath = os.path.join(self.workdir, "test0.properties")
        self.cnf_s = CNF_S
        self.cnf = CNF
        open(self.cpath, 'w').write(self.cnf_s)

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_loads(self):
        cnf = self.psr.loads(self.cnf_s)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_20_load(self):
        cnf = self.psr.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_30_dumps(self):
        cnf = self.psr.loads(self.cnf_s)
        cnf2 = self.psr.loads(self.psr.dumps(cnf))
        self.assertTrue(dicts_equal(cnf2, cnf), str(cnf2))

    def test_40_dump(self):
        cnf = self.psr.loads(self.cnf_s)
        self.psr.dump(cnf, self.cpath)
        cnf = self.psr.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

# vim:sw=4:ts=4:et:
