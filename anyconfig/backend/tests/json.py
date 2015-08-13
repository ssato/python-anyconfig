#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import os.path
import unittest

import anyconfig.backend.json as TT
import anyconfig.tests.common

from anyconfig.tests.common import dicts_equal


CNF_0_S = """{
  "a": 0,
  "b": "bbb",

  "sect0": {
    "c": ["x", "y", "z"]
  }
}
"""

CNF_0 = {'a': 0, 'b': 'bbb', 'sect0': {'c': ['x', 'y', 'z']}}


class Test10(unittest.TestCase):

    cnf = CNF_0
    cnf_s = CNF_0_S

    def test_00_supports(self):
        self.assertFalse(TT.Parser.supports("/a/b/c/d.ini"))
        self.assertTrue(TT.Parser.supports("/a/b/c/d.json"))

    def test_10_loads(self):
        cnf = TT.Parser.loads(self.cnf_s)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_30_dumps(self):
        cnf = TT.Parser.loads(TT.Parser.dumps(self.cnf))
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))


class Test20(unittest.TestCase):

    cnf = CNF_0
    cnf_s = CNF_0_S

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()
        self.cpath = os.path.join(self.workdir, "test0.json")
        open(self.cpath, 'w').write(self.cnf_s)

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_20_load(self):
        cnf = TT.Parser.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_22_load__optional_kwargs(self):
        cnf = TT.Parser.load(self.cpath, parse_int=None)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_40_dump(self):
        TT.Parser.dump(self.cnf, self.cpath)
        cnf = TT.Parser.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_42_dump_w_special_option(self):
        TT.Parser.dump(self.cnf, self.cpath, parse_int=None, indent=3)
        cnf = TT.Parser.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

# vim:sw=4:ts=4:et:
