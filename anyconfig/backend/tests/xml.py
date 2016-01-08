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
import anyconfig.backend.tests.ini
import anyconfig.tests.common

from anyconfig.tests.common import dicts_equal, to_bytes
from anyconfig.mdicts import to_container


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
        self.assertEqual(TT.etree_to_container(None, dict), {})

    def test_12_etree_to_container(self):
        cnf = TT.etree_to_container(self.root, to_container)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_20_container_to_etree__empty(self):
        # This should not happen but just in case.
        self.assertTrue(TT.container_to_etree("aaa", dict) is None)

    def test_22_container_to_etree(self):
        tree = TT.container_to_etree(self.cnf, to_container)
        buf = TT.BytesIO()
        tree.write(buf)
        cnf_s = buf.getvalue()
        self.assertEqual(cnf_s, self.cnf_s, cnf_s)


class Test10(anyconfig.backend.tests.ini.Test10):

    cnf = CNF_0
    cnf_s = CNF_0_S
    load_options = dump_options = dict(dummy="this will be ignored")

    def setUp(self):
        self.psr = TT.Parser()


class Test20(anyconfig.backend.tests.ini.Test20):

    psr_cls = TT.Parser
    cnf = CNF_0
    cnf_s = CNF_0_S
    cnf_fn = "conf0.xml"

    def setUp(self):
        self.psr = TT.Parser()
        self.workdir = anyconfig.tests.common.setup_workdir()
        self.cpath = os.path.join(self.workdir, self.cnf_fn)
        open(self.cpath, 'w').write(self.cnf_s)


# vim:sw=4:ts=4:et:
