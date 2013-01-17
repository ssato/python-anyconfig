#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.properties_ as T

import os
import tempfile
import unittest


CONF_0 = """
a = 0
b = bbb

sect0.c = x;y;z
"""

TEST_STRICT = False


if T.SUPPORTED:

    class Test_PropertiesParser(unittest.TestCase):

        def setUp(self):
            (_, conf) = tempfile.mkstemp(prefix="ac-test-")
            open(conf, 'w').write(CONF_0)
            self.config_path = conf

        def tearDown(self):
            os.remove(self.config_path)

        def test_00_supports(self):
            self.assertTrue(T.PropertiesParser.supports("/a/b/c/d.properties"))
            self.assertFalse(T.PropertiesParser.supports("/a/b/c/d.json"))

        def test_10_loads(self):
            """TODO: implement PropertiesParser.loads"""
            return

            c = T.PropertiesParser.loads(CONF_0)

            self.assertEquals(c['b'], "bbb", c)

            if TEST_STRICT:
                self.assertEquals(c['a'], 0, str(c))
                self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_20_load(self):
            c = T.PropertiesParser.load(self.config_path)

            self.assertEquals(c['b'], "bbb", c)

            if TEST_STRICT:
                self.assertEquals(c['a'], 0, str(c))
                self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])


# vim:sw=4:ts=4:et:
