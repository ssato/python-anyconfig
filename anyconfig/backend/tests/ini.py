#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, protected-access
from __future__ import absolute_import

import os.path
import unittest

import anyconfig.backend.ini as TT
import anyconfig.tests.common

from anyconfig.tests.common import dicts_equal


CNF_0_S = """[DEFAULT]
a: 0
b: bbb

[sect0]
c: x,y,z
"""

CNF_0 = {'DEFAULT': {'a': 0, 'b': 'bbb'},
         'sect0': {'a': 0, 'b': 'bbb', 'c': ['x', 'y', 'z']}}


class Test10(unittest.TestCase):

    cnf = CNF_0
    cnf_s = CNF_0_S
    load_options = dict(allow_no_value=False, defaults=None)
    dump_options = dict()

    def setUp(self):
        self.psr = TT.Parser()

    def test_10_loads(self):
        cnf = self.psr.loads(self.cnf_s)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_12_loads__w_options(self):
        cnf = self.psr.loads(self.cnf_s, **self.load_options)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_20_dumps(self):
        cnf = self.psr.loads(self.psr.dumps(self.cnf))
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_22_dumps__w_options(self):
        cnf = self.psr.loads(self.psr.dumps(self.cnf, **self.dump_options))
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))


class Test12(Test10):

    test_10_loads = test_12_loads__w_options = lambda: True
    test_20_loads = test_22_loads__w_options = lambda: True

    def test_12_loads__invalid_input(self):
        invalid_ini = "key=name"
        self.assertRaises(Exception, self.psr.loads, invalid_ini)


class Test20(unittest.TestCase):

    psr_cls = TT.Parser
    cnf = CNF_0
    cnf_s = CNF_0_S
    cnf_fn = "conf0.ini"

    def setUp(self):
        self.psr = self.psr_cls()
        self.workdir = anyconfig.tests.common.setup_workdir()
        self.cpath = os.path.join(self.workdir, self.cnf_fn)
        self.psr.wopen(self.cpath).write(self.cnf_s)

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_load(self):
        cnf = self.psr.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_20_dump(self):
        self.psr.dump(self.cnf, self.cpath)
        cnf = self.psr.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_30_load__from_stream(self):
        with self.psr.ropen(self.cpath) as strm:
            cnf = self.psr.load(strm)

        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_40_dump__to_stream(self):
        with self.psr.wopen(self.cpath) as strm:
            self.psr.dump(self.cnf, strm)

        cnf = self.psr.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

# vim:sw=4:ts=4:et:
