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


CONF_0 = """
a: 0
b: bbb

sect0:
  c: ["x", "y", "z"]
"""

if TT is not None:
    import yaml

    class Test(unittest.TestCase):

        def setUp(self):
            self.workdir = anyconfig.tests.common.setup_workdir()
            self.cpath = os.path.join(self.workdir, "test0.yml")
            open(self.cpath, 'w').write(CONF_0)

        def tearDown(self):
            anyconfig.tests.common.cleanup_workdir(self.workdir)

        def test_00_supports(self):
            self.assertFalse(TT.Parser.supports("/a/b/c/d.ini"))
            self.assertFalse(TT.Parser.supports("/a/b/c/d.json"))
            self.assertTrue(TT.Parser.supports("/a/b/c/d.yml"))

        def test_10_loads(self):
            cfg = TT.Parser.loads(CONF_0)

            self.assertEquals(cfg['a'], 0, str(cfg))
            self.assertEquals(cfg['b'], "bbb", cfg)
            self.assertEquals(cfg["sect0"]['c'], ['x', 'y', 'z'])

        def test_12_loads__safe(self):
            cfg = TT.Parser.loads(CONF_0, safe=True)

            self.assertEquals(cfg['a'], 0, str(cfg))
            self.assertEquals(cfg['b'], "bbb", cfg)
            self.assertEquals(cfg["sect0"]['c'], ['x', 'y', 'z'])

        def test_20_load(self):
            cfg = TT.Parser.load(self.cpath)

            self.assertEquals(cfg['a'], 0, str(cfg))
            self.assertEquals(cfg['b'], "bbb", cfg)
            self.assertEquals(cfg["sect0"]['c'], ['x', 'y', 'z'])

        def test_22_load__safe(self):
            cfg = TT.Parser.load(self.cpath, safe=True)

            self.assertEquals(cfg['a'], 0, str(cfg))
            self.assertEquals(cfg['b'], "bbb", cfg)
            self.assertEquals(cfg["sect0"]['c'], ['x', 'y', 'z'])

        def test_20_load__w_options(self):
            cfg = TT.Parser.load(self.cpath, Loader=yaml.loader.Loader)

            self.assertEquals(cfg['a'], 0, str(cfg))
            self.assertEquals(cfg['b'], "bbb", cfg)
            self.assertEquals(cfg["sect0"]['c'], ['x', 'y', 'z'])

        def test_30_dumps(self):
            cfg = TT.Parser.loads(CONF_0)
            cfg = TT.Parser.loads(TT.Parser.dumps(cfg))

            self.assertEquals(cfg['a'], 0, str(cfg))
            self.assertEquals(cfg['b'], "bbb", cfg)
            self.assertEquals(cfg["sect0"]['c'], ['x', 'y', 'z'])

        def test_32_dumps__safe(self):
            cfg = TT.Parser.loads(CONF_0)
            res = TT.Parser.dumps(cfg, safe=True)
            cfg = TT.Parser.loads(res)

            self.assertEquals(cfg['a'], 0, str(cfg))
            self.assertEquals(cfg['b'], "bbb", cfg)
            self.assertEquals(cfg["sect0"]['c'], ['x', 'y', 'z'])

        def test_40_dump(self):
            cfg = TT.Parser.loads(CONF_0)
            TT.Parser.dump(cfg, self.cpath)
            cfg = TT.Parser.load(self.cpath)

            self.assertEquals(cfg['a'], 0, str(cfg))
            self.assertEquals(cfg['b'], "bbb", cfg)
            self.assertEquals(cfg["sect0"]['c'], ['x', 'y', 'z'])

        def test_42_dump__safe(self):
            cfg = TT.Parser.loads(CONF_0)
            TT.Parser.dump(cfg, self.cpath, safe=True)
            cfg = TT.Parser.load(self.cpath)

            self.assertEquals(cfg['a'], 0, str(cfg))
            self.assertEquals(cfg['b'], "bbb", cfg)
            self.assertEquals(cfg["sect0"]['c'], ['x', 'y', 'z'])

        def test_40_dump__w_options(self):
            cfg = TT.Parser.loads(CONF_0)
            TT.Parser.dump(cfg, self.cpath, Dumper=yaml.dumper.Dumper)
            cfg = TT.Parser.load(self.cpath)

            self.assertEquals(cfg['a'], 0, str(cfg))
            self.assertEquals(cfg['b'], "bbb", cfg)
            self.assertEquals(cfg["sect0"]['c'], ['x', 'y', 'z'])

# vim:sw=4:ts=4:et:
