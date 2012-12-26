#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.yaml_ as T

import os
import tempfile
import unittest


CONF_0 = """
a: 0
b: bbb

sect0:
  c: ["x", "y", "z"]
"""


class Test_YamlConfigParser(unittest.TestCase):

    def setUp(self):
        (_, conf) = tempfile.mkstemp(prefix="ac-test-")
        open(conf, 'w').write(CONF_0)
        self.config_path = conf

    def tearDown(self):
        os.remove(self.config_path)

    def test_00_supports(self):
        self.assertFalse(T.YamlConfigParser.supports("/a/b/c/d.ini"))
        self.assertFalse(T.YamlConfigParser.supports("/a/b/c/d.json"))
        self.assertTrue(T.YamlConfigParser.supports("/a/b/c/d.yml"))

    def test_10_loads(self):

        c = T.YamlConfigParser.loads(CONF_0)

        self.assertEquals(c['a'], 0, str(c))
        self.assertEquals(c['b'], "bbb", c)
        self.assertEquals(c.a, 0)
        self.assertEquals(c.b, "bbb")

        self.assertEquals(c.sect0.c, ['x', 'y', 'z'])

    def test_20_load(self):

        c = T.YamlConfigParser.load(self.config_path)

        self.assertEquals(c['a'], 0, str(c))
        self.assertEquals(c['b'], "bbb", c)
        self.assertEquals(c.a, 0)
        self.assertEquals(c.b, "bbb")

        self.assertEquals(c.sect0.c, ['x', 'y', 'z'])


# vim:sw=4:ts=4:et:
