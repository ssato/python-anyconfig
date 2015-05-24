#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import os
import tempfile
import unittest

import anyconfig.backend.yaml_ as TT


CONF_0 = """
a: 0
b: bbb

sect0:
  c: ["x", "y", "z"]
"""

if TT.SUPPORTED:
    import yaml

    class Test_YamlConfigParser(unittest.TestCase):

        def setUp(self):
            (_, conf) = tempfile.mkstemp(prefix="ac-test-")
            open(conf, 'w').write(CONF_0)
            self.config_path = conf

        def tearDown(self):
            os.remove(self.config_path)

        def test_00_supports(self):
            self.assertFalse(TT.YamlConfigParser.supports("/a/b/c/d.ini"))
            self.assertFalse(TT.YamlConfigParser.supports("/a/b/c/d.json"))
            self.assertTrue(TT.YamlConfigParser.supports("/a/b/c/d.yml"))

        def test_10_loads(self):
            c = TT.YamlConfigParser.loads(CONF_0)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_12_loads__safe(self):
            c = TT.YamlConfigParser.loads(CONF_0, safe=True)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_20_load(self):
            c = TT.YamlConfigParser.load(self.config_path)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_22_load__safe(self):
            c = TT.YamlConfigParser.load(self.config_path, safe=True)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_20_load__w_options(self):
            c = TT.YamlConfigParser.load(self.config_path,
                                         Loader=yaml.loader.Loader)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_30_dumps(self):
            c = TT.YamlConfigParser.loads(CONF_0)
            s = TT.YamlConfigParser.dumps(c)
            c = TT.YamlConfigParser.loads(s)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_32_dumps__safe(self):
            c = TT.YamlConfigParser.loads(CONF_0)
            s = TT.YamlConfigParser.dumps(c, safe=True)
            c = TT.YamlConfigParser.loads(s)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_40_dump(self):
            c = TT.YamlConfigParser.loads(CONF_0)
            TT.YamlConfigParser.dump(c, self.config_path)
            c = TT.YamlConfigParser.load(self.config_path)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_42_dump__safe(self):
            c = TT.YamlConfigParser.loads(CONF_0)
            TT.YamlConfigParser.dump(c, self.config_path, safe=True)
            c = TT.YamlConfigParser.load(self.config_path)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_40_dump__w_options(self):
            c = TT.YamlConfigParser.loads(CONF_0)
            TT.YamlConfigParser.dump(c, self.config_path,
                                     Dumper=yaml.dumper.Dumper)
            c = TT.YamlConfigParser.load(self.config_path)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

# vim:sw=4:ts=4:et:
