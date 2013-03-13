#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.ini_ as I

import os
import tempfile
import unittest


CONF_0 = """[DEFAULT]
a: 0
b: bbb

[sect0]
c: x,y,z
"""


class Test_IniConfigParser(unittest.TestCase):

    def setUp(self):
        (_, conf) = tempfile.mkstemp(prefix="ac-test-")
        open(conf, 'w').write(CONF_0)
        self.config_path = conf

    def tearDown(self):
        os.remove(self.config_path)

    def test_00_supports(self):
        self.assertTrue(I.IniConfigParser.supports("/a/b/c/d.ini"))
        self.assertFalse(I.IniConfigParser.supports("/a/b/c/d.json"))

    def test_10_loads(self):

        c = I.IniConfigParser.loads(CONF_0)
        self.assertEquals(c["DEFAULT"]['a'], 0, str(c))
        self.assertEquals(c["DEFAULT"]['b'], "bbb", c)
        self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

    def test_20_load(self):

        c = I.IniConfigParser.load(self.config_path)
        self.assertEquals(c["DEFAULT"]['a'], 0, str(c))
        self.assertEquals(c["DEFAULT"]['b'], "bbb", c)
        self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

    def test_30_dumps(self):

        c = I.IniConfigParser.loads(CONF_0)
        d = I.IniConfigParser.dumps(c)
        c2 = I.IniConfigParser.loads(d)

        self.assertEquals(c2["DEFAULT"]['a'], c["DEFAULT"]['a'], str(c2))
        self.assertEquals(c2["DEFAULT"]['b'], c["DEFAULT"]['b'], str(c2))
        self.assertEquals(c2["sect0"]['c'], c["sect0"]['c'], str(c2))

    def test_40_dump(self):

        c = I.IniConfigParser.loads(CONF_0)
        d = I.IniConfigParser.dump(c, self.config_path)
        c2 = I.IniConfigParser.load(self.config_path)

        self.assertEquals(c2["DEFAULT"]['a'], c["DEFAULT"]['a'], str(c2))
        self.assertEquals(c2["DEFAULT"]['b'], c["DEFAULT"]['b'], str(c2))
        self.assertEquals(c2["sect0"]['c'], c["sect0"]['c'], str(c2))

# vim:sw=4:ts=4:et:
