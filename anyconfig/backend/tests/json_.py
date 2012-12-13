#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.json_ as T

import os
import tempfile
import unittest


CONF_0 = """{
  "a": 0,
  "b": "bbb",

  "sect0": {
    "c": ["x", "y", "z"]
  }
}
"""


class Test_JsonConfigParser(unittest.TestCase):

    def setUp(self):
        (_, conf) = tempfile.mkstemp(prefix="ac-test-")
        open(conf, 'w').write(CONF_0)
        self.config_path = conf

    def tearDown(self):
        os.remove(self.config_path)

    def test_00_supports(self):
        self.assertFalse(T.JsonConfigParser.supports("/a/b/c/d.ini"))
        self.assertTrue(T.JsonConfigParser.supports("/a/b/c/d.json"))

    def test_10_load(self):

        c = T.JsonConfigParser.load(self.config_path)

        self.assertEquals(c['a'], 0, str(c))
        self.assertEquals(c['b'], "bbb", c)
        self.assertEquals(c.a, 0)
        self.assertEquals(c.b, "bbb")

        self.assertEquals(c.sect0.c, ['x', 'y', 'z'])

# vim:sw=4:ts=4:et:
