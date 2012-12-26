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
        print str(c)
        self.assertEquals(c['a'], 0, str(c))
        self.assertEquals(c['b'], "bbb", c)
        self.assertEquals(c.a, 0)
        self.assertEquals(c.b, "bbb")

        self.assertEquals(c.sect0.c, ['x', 'y', 'z'])

    def test_20_load(self):

        c = I.IniConfigParser.load(self.config_path)
        print str(c)
        self.assertEquals(c['a'], 0, str(c))
        self.assertEquals(c['b'], "bbb", c)
        self.assertEquals(c.a, 0)
        self.assertEquals(c.b, "bbb")

        self.assertEquals(c.sect0.c, ['x', 'y', 'z'])

# vim:sw=4:ts=4:et:
