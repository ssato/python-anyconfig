#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import os.path
import unittest

import anyconfig.backend.xml as TT
import anyconfig.tests.common


CONF_0 = """<?xml version="1.0" encoding="UTF-8"?>
<config name='foo'>
  <a>0</a>
  <b id="b0">bbb</b>
  <sect0>
    <c>x, y, z</c>
  </sect0>
</config>
"""


class Test(unittest.TestCase):

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()
        self.cpath = os.path.join(self.workdir, "test0.xml")
        open(self.cpath, 'w').write(CONF_0)

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_00_supports(self):
        self.assertFalse(TT.Parser.supports("/a/b/c/d.ini"))
        self.assertTrue(TT.Parser.supports("/a/b/c/d.xml"))

    def test_10_loads(self):
        cfg = TT.Parser.loads(CONF_0)

        self.assertTrue("config" in cfg)
        self.assertTrue("attrs" in cfg["config"])
        self.assertTrue("name" in cfg["config"]["attrs"])
        self.assertEquals(cfg["config"]["attrs"].get("name", None), "foo")

        self.assertTrue(isinstance(cfg["config"]["children"], list))
        self.assertNotEquals(cfg["config"]["children"], [])

        self.assertTrue('a' in cfg["config"]["children"][0])
        self.assertTrue("text" in cfg["config"]["children"][0]['a'])
        self.assertTrue("attrs" not in cfg["config"]["children"][0]['a'])
        self.assertEquals(cfg["config"]["children"][0]['a']["text"], '0')

        self.assertTrue('b' in cfg["config"]["children"][1])
        self.assertTrue("text" in cfg["config"]["children"][1]['b'])
        self.assertTrue("attrs" in cfg["config"]["children"][1]['b'])
        self.assertEquals(cfg["config"]["children"][1]['b']["text"], "bbb")
        self.assertTrue("id" in cfg["config"]["children"][1]['b']["attrs"])
        self.assertEquals(cfg["config"]["children"][1]['b']["attrs"]["id"],
                          "b0")

        self.assertTrue('sect0' in cfg["config"]["children"][2])
        self.assertTrue("text" not in cfg["config"]["children"][2]['sect0'])
        self.assertTrue("attrs" not in cfg["config"]["children"][2]['sect0'])
        self.assertTrue("children" in cfg["config"]["children"][2]['sect0'])
        self.assertTrue(cfg["config"]["children"][2]['sect0']["children"])

    def test_20_load(self):
        """FIXME: Implement test cases for Parser.load"""
        # c = TT.Parser.load(self.cpath)["config"]

        # self.assertEquals(c['a'], 0, str(c))
        # self.assertEquals(c['b'], "bbb", c)
        pass

    def test_30_dumps_impl(self):
        try:
            TT.Parser.dumps_impl({})
            raise RuntimeError("test_30_dumps_impl: "
                               "NotImplementedError was not raised!")
        except NotImplementedError:
            pass

# vim:sw=4:ts=4:et:
