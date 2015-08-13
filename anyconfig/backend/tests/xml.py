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
from anyconfig.tests.common import dicts_equal


CNF_0_S = """<?xml version="1.0" encoding="UTF-8"?>
<config name='foo'>
  <a>0</a>
  <b id="b0">bbb</b>
  <sect0>
    <c>x, y, z</c>
  </sect0>
</config>
"""

CNF_0 = {'config': {'@attrs': {'name': 'foo'},
                    '@children': [{'a': {'@text': '0'}},
                                  {'b': {'@attrs': {'id': 'b0'},
                                         '@text': 'bbb'}},
                                  {'sect0': {
                                      '@children': [{'c': {
                                          '@text': 'x, y, z'
                                      }}]}}]}}


class Test(unittest.TestCase):

    cnf = CNF_0
    cnf_s = CNF_0_S

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()
        self.cpath = os.path.join(self.workdir, "test0.xml")
        open(self.cpath, 'w').write(self.cnf_s)

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_00_supports(self):
        self.assertFalse(TT.Parser.supports("/a/b/c/d.ini"))
        self.assertTrue(TT.Parser.supports("/a/b/c/d.xml"))

    def test_10_loads(self):
        cnf = TT.Parser.loads(self.cnf_s)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

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
