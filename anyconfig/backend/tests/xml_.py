#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.xml_ as TT

import os
import tempfile
import unittest


CONF_0 = """<?xml version="1.0" encoding="UTF-8"?>
<config name='foo'>
  <a>0</a>
  <b id="b0">bbb</b>
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
        self.assertFalse(TT.XmlConfigParser.supports("/a/b/c/d.ini"))
        self.assertTrue(TT.XmlConfigParser.supports("/a/b/c/d.xml"))

    def test_10_loads(self):
        """FIXME: Implement test cases for XmlConfigParser.loads"""
        c = TT.XmlConfigParser.loads(CONF_0)
        # container = TT.XmlConfigParser.container()

        self.assertTrue("config" in c)
        self.assertTrue("attrs" in c["config"])
        self.assertTrue("name" in c["config"]["attrs"])
        self.assertEquals(c["config"]["attrs"].get("name", None), "foo")

        self.assertTrue(isinstance(c["config"]["children"], list))
        self.assertNotEquals(c["config"]["children"], [])

        self.assertTrue('a' in c["config"]["children"][0])
        self.assertTrue("text" in c["config"]["children"][0]['a'])
        self.assertTrue("attrs" not in c["config"]["children"][0]['a'])
        self.assertEquals(c["config"]["children"][0]['a']["text"], '0')

        self.assertTrue('b' in c["config"]["children"][1])
        self.assertTrue("text" in c["config"]["children"][1]['b'])
        self.assertTrue("attrs" in c["config"]["children"][1]['b'])
        self.assertEquals(c["config"]["children"][1]['b']["text"], "bbb")
        self.assertTrue("id" in c["config"]["children"][1]['b']["attrs"])
        self.assertEquals(c["config"]["children"][1]['b']["attrs"]["id"], "b0")

        self.assertTrue('sect0' in c["config"]["children"][2])
        self.assertTrue("text" not in c["config"]["children"][2]['sect0'])
        self.assertTrue("attrs" not in c["config"]["children"][2]['sect0'])
        self.assertTrue("children" in c["config"]["children"][2]['sect0'])
        self.assertTrue(c["config"]["children"][2]['sect0']["children"])

    def test_20_load(self):
        """FIXME: Implement test cases for XmlConfigParser.load"""
        # c = TT.XmlConfigParser.load(self.config_path)["config"]

        # self.assertEquals(c['a'], 0, str(c))
        # self.assertEquals(c['b'], "bbb", c)
        pass

    def test_30_dumps_impl(self):
        try:
            TT.XmlConfigParser.dumps_impl({})
            raise RuntimeError("test_30_dumps_impl: "
                               "NotImplementedError was not raised!")
        except NotImplementedError:
            pass

# vim:sw=4:ts=4:et:
