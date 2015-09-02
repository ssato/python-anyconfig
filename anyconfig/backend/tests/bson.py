#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import os.path
import unittest

import anyconfig.backend.bson as TT
import anyconfig.tests.common
import anyconfig.compat

from anyconfig.tests.common import dicts_equal, to_bytes as _bytes


CNF_0 = {"a": 0.1,
         "b": _bytes("bbb"),
         "sect0": {"c": [_bytes("x"), _bytes("y"), _bytes("z")]}}


class Test10(unittest.TestCase):

    def setUp(self):
        self.psr = TT.Parser()
        self.cnf = CNF_0
        self.cnf_s = TT.bson.BSON.encode(self.cnf)

    def test_10_loads(self):
        cnf = self.psr.loads(self.cnf_s)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_12_loads__optional_kwargs(self):
        cnf = self.psr.loads(self.cnf_s, as_class=dict)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_30_dumps(self):
        cnf = self.psr.loads(self.psr.dumps(self.cnf))
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_32_dump_w_special_option(self):
        cnf = self.psr.loads(self.psr.dumps(self.cnf, check_keys=True))
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))


class Test20(unittest.TestCase):

    def setUp(self):
        self.psr = TT.Parser()
        self.cnf = CNF_0
        self.cnf_s = TT.bson.BSON.encode(self.cnf)
        self.workdir = anyconfig.tests.common.setup_workdir()
        self.cpath = os.path.join(self.workdir, "test0.bson")
        open(self.cpath, 'wb').write(self.cnf_s)

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_20_load(self):
        cnf = self.psr.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_30_load__from_stream(self):
        with open(self.cpath) as stream:
            cnf = self.psr.load(stream)

        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_40_dump(self):
        self.psr.dump(self.cnf, self.cpath)
        cnf = self.psr.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_50_dump(self):
        with open(self.cpath, 'w') as stream:
            self.psr.dump(self.cnf, stream)

        cnf = self.psr.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

# vim:sw=4:ts=4:et:
