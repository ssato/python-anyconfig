#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import copy

import anyconfig.backend.msgpack as TT
import anyconfig.backend.tests.ini

from anyconfig.compat import OrderedDict as ODict, IS_PYTHON_3
from anyconfig.tests.common import dicts_equal, to_bytes as _bytes


CNF_0 = ODict(((_bytes("a"), 0.1),
               (_bytes("b"), _bytes("bbb")),
               (_bytes("sect0"),
                ODict(((_bytes("c"),
                        [_bytes("x"), _bytes("y"), _bytes("z")]), )))))


class Test10(anyconfig.backend.tests.ini.Test10):

    cnf = CNF_0
    cnf_s = TT.msgpack.packb(CNF_0)

    if IS_PYTHON_3:
        is_order_kept = False  # FIXME: Make it work w/ python 3.

    def setUp(self):
        self.psr = TT.Parser()

    def test_12_loads__w_options(self):
        cnf = self.psr.loads(self.cnf_s, use_list=False)
        ref = copy.deepcopy(self.cnf)
        ref[_bytes("sect0")][_bytes("c")] = (_bytes("x"), _bytes("y"),
                                             _bytes("z"))
        self.assertTrue(dicts_equal(cnf, ref), str(cnf))

    def test_22_dumps__w_options(self):
        cnf = self.psr.loads(self.psr.dumps(self.cnf, use_single_float=True))
        ref = copy.deepcopy(self.cnf)
        ref[_bytes("a")] = cnf[_bytes("a")]  # single float value.
        self.assertFalse(dicts_equal(cnf, self.cnf), str(cnf))
        self.assertTrue(dicts_equal(cnf, ref), str(cnf))


class Test20(anyconfig.backend.tests.ini.Test20):

    psr_cls = TT.Parser
    cnf = CNF_0
    cnf_s = TT.msgpack.packb(CNF_0)
    cnf_fn = "conf0.msgpack"

    def test_12_load__w_options(self):
        cnf = self.psr.load(self.cpath, use_list=False)
        ref = copy.deepcopy(self.cnf)
        ref[_bytes("sect0")][_bytes("c")] = (_bytes("x"), _bytes("y"),
                                             _bytes("z"))
        self.assertTrue(dicts_equal(cnf, ref), str(cnf))

    def test_22_dump_w_special_option(self):
        self.psr.dump(self.cnf, self.cpath, use_single_float=True)
        cnf = self.psr.load(self.cpath)
        ref = copy.deepcopy(self.cnf)
        ref[_bytes("a")] = cnf[_bytes("a")]  # single float value.
        self.assertFalse(dicts_equal(cnf, self.cnf), str(cnf))
        self.assertTrue(dicts_equal(cnf, ref), str(cnf))

# vim:sw=4:ts=4:et:
