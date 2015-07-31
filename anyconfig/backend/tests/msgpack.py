#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import os.path
import unittest

import anyconfig.backend.msgpack as TT
import anyconfig.tests.common
import anyconfig.compat


CONF_0 = {"a": 0.1,
          "b": "bbb",
          "sect0": {"c": ["x", "y", "z"]}}


def _b(astr):
    return bytes(astr, 'utf-8') if anyconfig.compat.IS_PYTHON_3 else astr


class Test(unittest.TestCase):

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()
        self.cpath = os.path.join(self.workdir, "test0.msgpack")
        self.packed = TT.msgpack.packb(CONF_0)
        open(self.cpath, 'wb').write(self.packed)

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_loads(self):
        cfg = TT.Parser.loads(self.packed)

        self.assertEquals(cfg[_b('a')], 0.1, str(cfg))
        self.assertEquals(cfg[_b('b')], _b("bbb"), cfg)
        self.assertEquals(cfg[_b('sect0')][_b('c')],
                          [_b('x'), _b('y'), _b('z')])

    def test_20_load(self):
        cfg = TT.Parser.load(self.cpath)

        self.assertEquals(cfg[_b('a')], 0.1, str(cfg))
        self.assertEquals(cfg[_b('b')], _b("bbb"), cfg)
        self.assertEquals(cfg[_b('sect0')][_b('c')],
                          [_b('x'), _b('y'), _b('z')])

    def test_22_load__optional_kwargs(self):
        cfg = TT.Parser.load(self.cpath, use_list=False)

        self.assertEquals(cfg[_b('a')], 0.1, str(cfg))
        self.assertEquals(cfg[_b('b')], _b("bbb"), cfg)
        self.assertEquals(cfg[_b('sect0')][_b('c')],
                          (_b('x'), _b('y'), _b('z')))

    def test_30_dumps(self):
        cfg = TT.Parser.loads(self.packed)
        cfg2 = TT.Parser.loads(TT.Parser.dumps(cfg))

        self.assertEquals(cfg2[_b('a')], 0.1, str(cfg))
        self.assertEquals(cfg2[_b('b')], _b("bbb"), cfg)
        self.assertEquals(cfg2[_b('sect0')][_b('c')],
                          [_b('x'), _b('y'), _b('z')])

    def test_40_dump(self):
        cfg = TT.Parser.loads(self.packed)
        TT.Parser.dump(cfg, self.cpath)
        cfg = TT.Parser.load(self.cpath)

        self.assertEquals(cfg[_b('a')], 0.1, str(cfg))
        self.assertEquals(cfg[_b('b')], _b("bbb"), cfg)
        self.assertEquals(cfg[_b('sect0')][_b('c')],
                          [_b('x'), _b('y'), _b('z')])

    def test_42_dump_w_special_option(self):
        cfg = TT.Parser.loads(self.packed)
        TT.Parser.dump(cfg, self.cpath, use_single_float=True)
        cfg = TT.Parser.load(self.cpath)

        self.assertNotEquals(cfg[_b('a')], 0.1, str(cfg))
        self.assertEquals(cfg[_b('b')], _b("bbb"), cfg)
        self.assertEquals(cfg[_b('sect0')][_b('c')],
                          [_b('x'), _b('y'), _b('z')])

# vim:sw=4:ts=4:et:
