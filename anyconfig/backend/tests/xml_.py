#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.xml_ as T

import os
import tempfile
import unittest


CONF_0 = """<?xml version="1.0" encoding="UTF-8"?>
<config>
  <a>0</a>
  <b>"bbb"</b>
  <sect0>
    <c>x, y, z</c>
  </sect0>
</config>
"""


class Test_XmlConfigParser(unittest.TestCase):

    def setUp(self):
        (_, conf) = tempfile.mkstemp(prefix="ac-test-")
        open(conf, 'w').write(CONF_0)
        self.config_path = conf

    def tearDown(self):
        os.remove(self.config_path)

    def test_00_supports(self):
        self.assertFalse(T.XmlConfigParser.supports("/a/b/c/d.ini"))
        self.assertTrue(T.XmlConfigParser.supports("/a/b/c/d.xml"))

    def test_10_loads(self):
        """FIXME: Implement test cases for XmlConfigParser.loads"""
        return

        c = T.XmlConfigParser.loads(CONF_0)["config"]

        self.assertEquals(c['a'], 0, str(c))
        self.assertEquals(c['b'], "bbb", c)
        self.assertEquals(c.a, 0)
        self.assertEquals(c.b, "bbb")

        # FIXME: Needs to implement list parser ?
        #self.assertEquals(c.sect0.c, ['x', 'y', 'z'])

    def test_20_load(self):
        """FIXME: Implement test cases for XmlConfigParser.load"""
        return

        c = T.XmlConfigParser.load(self.config_path)["config"]

        self.assertEquals(c['a'], 0, str(c))
        self.assertEquals(c['b'], "bbb", c)
        self.assertEquals(c.a, 0)
        self.assertEquals(c.b, "bbb")

        #self.assertEquals(c.sect0.c, ['x', 'y', 'z'])


# vim:sw=4:ts=4:et:
