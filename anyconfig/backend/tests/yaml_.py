#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.yaml_ as T
# import anyconfig.tests.common as C

import os
# import sys
import tempfile
import unittest


CONF_0 = """
a: 0
b: bbb

sect0:
  c: ["x", "y", "z"]
"""

if T.SUPPORTED:
    import yaml

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
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_12_loads__safe(self):
            c = T.YamlConfigParser.loads(CONF_0, safe=True)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_20_load(self):
            c = T.YamlConfigParser.load(self.config_path)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_22_load__safe(self):
            c = T.YamlConfigParser.load(self.config_path, safe=True)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_20_load__w_options(self):
            c = T.YamlConfigParser.load(self.config_path,
                                        Loader=yaml.loader.Loader)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_30_dumps(self):
            c = T.YamlConfigParser.loads(CONF_0)
            s = T.YamlConfigParser.dumps(c)
            c = T.YamlConfigParser.loads(s)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_32_dumps__safe(self):
            c = T.YamlConfigParser.loads(CONF_0)
            s = T.YamlConfigParser.dumps(c, safe=True)
            c = T.YamlConfigParser.loads(s)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_40_dump(self):
            c = T.YamlConfigParser.loads(CONF_0)
            T.YamlConfigParser.dump(c, self.config_path)
            c = T.YamlConfigParser.load(self.config_path)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_42_dump__safe(self):
            c = T.YamlConfigParser.loads(CONF_0)
            T.YamlConfigParser.dump(c, self.config_path, safe=True)
            c = T.YamlConfigParser.load(self.config_path)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

        def test_40_dump__w_options(self):
            c = T.YamlConfigParser.loads(CONF_0)
            T.YamlConfigParser.dump(c, self.config_path,
                                    Dumper=yaml.dumper.Dumper)
            c = T.YamlConfigParser.load(self.config_path)

            self.assertEquals(c['a'], 0, str(c))
            self.assertEquals(c['b'], "bbb", c)
            self.assertEquals(c["sect0"]['c'], ['x', 'y', 'z'])

# TODO: Implement test cases if necessary modules are missing.
#
#    class Test_ImportError(unittest.TestCase):
#        def test_00_ImportError(self):
#            C.mask_modules("yaml")
#
#            del sys.modules[T.__name__]
#
#            import anyconfig.backend.yaml_ as X
#            self.assertFalse(X.SUPPORTED)
#
# vim:sw=4:ts=4:et:
