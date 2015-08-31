#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
from __future__ import absolute_import

import copy
import os.path
import unittest

import anyconfig.backend.xml as TT
import anyconfig.tests.common
from anyconfig.tests.common import dicts_equal, to_bytes


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


class Test00(unittest.TestCase):

    def setUp(self):
        self.root = TT.ET.Element("config", attrib=dict(name="foo"))
        celm0 = TT.ET.SubElement(self.root, "a")
        celm0.text = '0'
        celm1 = TT.ET.SubElement(self.root, "b", attrib=dict(id="b0", ))
        celm1.text = "bbb"
        self.tree = TT.ET.ElementTree(self.root)

        self.cnf = copy.deepcopy(CNF_0)
        del self.cnf["config"]["@children"][-1]

        self.cnf_s = to_bytes('<config name="foo"><a>0</a>'
                              '<b id="b0">bbb</b></config>')

    def test_10_etree_to_container__empty(self):
        self.assertEquals(TT.etree_to_container(None, dict), {})

    def test_12_etree_to_container(self):
        cnf = TT.etree_to_container(self.root, TT.Parser().container())
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_20_container_to_etree__empty(self):
        # This should not happen but just in case.
        self.assertTrue(TT.container_to_etree("aaa", dict) is None)

    def test_22_container_to_etree(self):
        tree = TT.container_to_etree(self.cnf, TT.Parser().container())
        buf = TT.BytesIO()
        tree.write(buf)
        cnf_s = buf.getvalue()
        self.assertEquals(cnf_s, self.cnf_s, cnf_s)


class Test10(unittest.TestCase):

    cnf = CNF_0
    cnf_s = CNF_0_S

    def test_20_loads(self):
        cnf = TT.Parser().loads(self.cnf_s)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_30_dumps(self):
        cnf = TT.Parser().loads(TT.Parser().dumps(self.cnf))
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))


class Test20(unittest.TestCase):

    cnf = CNF_0
    cnf_s = CNF_0_S

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()
        self.cpath = os.path.join(self.workdir, "test0.xml")
        open(self.cpath, 'w').write(self.cnf_s)

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_load(self):
        cnf = TT.Parser().load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_20_dump(self):
        TT.Parser().dump(self.cnf, self.cpath)
        cnf = TT.Parser().load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

# vim:sw=4:ts=4:et:
