#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import os.path
import unittest

try:
    import anyconfig.backend.yaml as TT
except ImportError:
    TT = None

import anyconfig.tests.common
from anyconfig.tests.common import dicts_equal


CNF_0_S = """
a: 0
b: bbb

sect0:
  c: ["x", "y", "z"]
"""

CNF_0 = {'a': 0, 'b': 'bbb', 'sect0': {'c': ['x', 'y', 'z']}}


if TT is not None:
    import yaml

    class Test(unittest.TestCase):

        cnf = CNF_0
        cnf_s = CNF_0_S

        def setUp(self):
            self.workdir = anyconfig.tests.common.setup_workdir()
            self.cpath = os.path.join(self.workdir, "test0.yml")
            open(self.cpath, 'w').write(self.cnf_s)

        def tearDown(self):
            anyconfig.tests.common.cleanup_workdir(self.workdir)

        def test_10_loads(self):
            cnf = TT.Parser.loads(self.cnf_s)
            self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

        def test_12_loads__safe(self):
            cnf = TT.Parser.loads(self.cnf_s, safe=True)
            self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

        def test_20_load(self):
            cnf = TT.Parser.load(self.cpath)
            self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

        def test_22_load__safe(self):
            cnf = TT.Parser.load(self.cpath, safe=True)
            self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

        def test_20_load__w_options(self):
            cnf = TT.Parser.load(self.cpath, Loader=yaml.loader.Loader)
            self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

        def test_30_dumps(self):
            cnf = TT.Parser.loads(TT.Parser.dumps(self.cnf))
            self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

        def test_32_dumps__safe(self):
            cnf = TT.Parser.loads(TT.Parser.dumps(self.cnf, safe=True))
            self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

        def test_40_dump(self):
            TT.Parser.dump(self.cnf, self.cpath)
            cnf = TT.Parser.load(self.cpath)
            self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

        def test_42_dump__safe(self):
            TT.Parser.dump(self.cnf, self.cpath, safe=True)
            cnf = TT.Parser.load(self.cpath)
            self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

        def test_40_dump__w_options(self):
            TT.Parser.dump(self.cnf, self.cpath, Dumper=yaml.dumper.Dumper)
            cnf = TT.Parser.load(self.cpath)
            self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

# vim:sw=4:ts=4:et:
