#
# Copyright (C) 2012, 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import os.path
import unittest

import anyconfig.backend.ini_ as TT
import anyconfig.tests.common


CONF_0 = """[DEFAULT]
a: 0
b: bbb

[sect0]
c: x,y,z
"""


class Test(unittest.TestCase):

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()
        self.cpath = os.path.join(self.workdir, "conf0.ini")
        open(self.cpath, 'w').write(CONF_0)

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_loads(self):
        cfg = TT.IniConfigParser.loads(CONF_0)
        self.assertEquals(cfg["DEFAULT"]['a'], 0, str(cfg))
        self.assertEquals(cfg["DEFAULT"]['b'], "bbb", cfg)
        self.assertEquals(cfg["sect0"]['c'], ['x', 'y', 'z'])

    def test_20_load(self):
        cfg = TT.IniConfigParser.load(self.cpath)
        self.assertEquals(cfg["DEFAULT"]['a'], 0, str(cfg))
        self.assertEquals(cfg["DEFAULT"]['b'], "bbb", cfg)
        self.assertEquals(cfg["sect0"]['c'], ['x', 'y', 'z'])

    def test_22_load__invalid_ini(self):
        invalid_ini = "key=name"
        self.assertRaises(Exception, TT.IniConfigParser.loads, invalid_ini)

    def test_20_load__w_options(self):
        cfg = TT.IniConfigParser.load(self.cpath, allow_no_value=False)
        self.assertEquals(cfg["DEFAULT"]['a'], 0, str(cfg))
        self.assertEquals(cfg["DEFAULT"]['b'], "bbb", cfg)
        self.assertEquals(cfg["sect0"]['c'], ['x', 'y', 'z'])

    def test_30_dumps(self):
        cfg = TT.IniConfigParser.loads(CONF_0)
        cfg2 = TT.IniConfigParser.loads(TT.IniConfigParser.dumps(cfg))

        self.assertEquals(cfg2["DEFAULT"]['a'], cfg["DEFAULT"]['a'], str(cfg2))
        self.assertEquals(cfg2["DEFAULT"]['b'], cfg["DEFAULT"]['b'], str(cfg2))
        self.assertEquals(cfg2["sect0"]['c'], cfg["sect0"]['c'], str(cfg2))

    def test_40_dump(self):
        cfg = TT.IniConfigParser.loads(CONF_0)
        TT.IniConfigParser.dump(cfg, self.cpath)
        cfg2 = TT.IniConfigParser.load(self.cpath)

        self.assertEquals(cfg2["DEFAULT"]['a'], cfg["DEFAULT"]['a'], str(cfg2))
        self.assertEquals(cfg2["DEFAULT"]['b'], cfg["DEFAULT"]['b'], str(cfg2))
        self.assertEquals(cfg2["sect0"]['c'], cfg["sect0"]['c'], str(cfg2))

# vim:sw=4:ts=4:et:
