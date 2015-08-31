#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import copy
import os.path
import unittest

import anyconfig.backend.msgpack as TT
import anyconfig.tests.common
import anyconfig.compat

from anyconfig.tests.common import dicts_equal, to_bytes as _bytes


CNF_0 = {_bytes("a"): 0.1,
         _bytes("b"): _bytes("bbb"),
         _bytes("sect0"): {_bytes("c"): [_bytes("x"), _bytes("y"),
                                         _bytes("z")]}}


class Test(unittest.TestCase):

    def setUp(self):
        self.cnf = CNF_0
        self.workdir = anyconfig.tests.common.setup_workdir()
        self.cpath = os.path.join(self.workdir, "test0.msgpack")
        self.packed = TT.msgpack.packb(self.cnf)
        open(self.cpath, 'wb').write(self.packed)

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_loads(self):
        cnf = TT.Parser().loads(self.packed)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_20_load(self):
        cnf = TT.Parser().load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_22_load__optional_kwargs(self):
        cnf = TT.Parser().load(self.cpath, use_list=False)
        ref = copy.deepcopy(self.cnf)
        ref[_bytes("sect0")][_bytes("c")] = (_bytes("x"), _bytes("y"),
                                             _bytes("z"))
        self.assertTrue(dicts_equal(cnf, ref), str(cnf))

    def test_30_dumps(self):
        cnf = TT.Parser().loads(TT.Parser().dumps(self.cnf))
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_40_dump(self):
        TT.Parser().dump(self.cnf, self.cpath)
        cnf = TT.Parser().load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_42_dump_w_special_option(self):
        TT.Parser().dump(self.cnf, self.cpath, use_single_float=True)
        cnf = TT.Parser().load(self.cpath)
        ref = copy.deepcopy(self.cnf)
        ref[_bytes("a")] = cnf[_bytes("a")]  # single float value.
        self.assertFalse(dicts_equal(cnf, self.cnf), str(cnf))
        self.assertTrue(dicts_equal(cnf, ref), str(cnf))

# vim:sw=4:ts=4:et:
