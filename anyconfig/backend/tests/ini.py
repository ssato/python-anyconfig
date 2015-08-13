#
# Copyright (C) 2012, 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
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

    def test_10_loads(self):
        cnf = TT.Parser.loads(self.cnf_s)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_12_loads__invalid_input(self):
        invalid_ini = "key=name"
        self.assertRaises(Exception, TT.Parser.loads, invalid_ini)

    def test_14_loads__w_options(self):
        cnf = TT.Parser.loads(self.cnf_s, allow_no_value=False)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_20_dumps(self):
        cnf = TT.Parser.loads(TT.Parser.dumps(self.cnf))
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))


class Test20(unittest.TestCase):

    cnf = CNF_0
    cnf_s = CNF_0_S

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()
        self.cpath = os.path.join(self.workdir, "conf0.ini")
        open(self.cpath, 'w').write(self.cnf_s)

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_load(self):
        cnf = TT.Parser.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_20_dump(self):
        TT.Parser.dump(self.cnf, self.cpath)
        cnf = TT.Parser.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

# vim:sw=4:ts=4:et:
