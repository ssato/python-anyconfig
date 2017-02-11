#
# Copyright (C) 2012 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, protected-access
from __future__ import absolute_import
import os.path
import unittest

import anyconfig.backend.xml as TT
import anyconfig.backend.tests.ini
import anyconfig.tests.common
import anyconfig.compat

from anyconfig.tests.common import dicts_equal, to_bytes


XML_W_NS_S = """
<a xmlns="http://example.com/ns/config"
   xmlns:val="http://example.com/ns/config/val">
   <b>1</b>
   <val:c>C</val:c>
</a>
"""

CNF_0 = {'config': {'@attrs': {'name': 'foo'},
                    '@children': [{'a': '0'},
                                  {'b': {'@attrs': {'id': 'b0'},
                                         '@text': 'bbb'}},
                                  {'sect0': {'c': 'x, y, z'}}]}}
CNF_0_S = """\
<?xml version="1.0" encoding="UTF-8"?>
<config name='foo'>
  <a>0</a>
  <b id="b0">bbb</b>
  <sect0>
    <c>x, y, z</c>
  </sect0>
</config>
"""


class Test_00(unittest.TestCase):

    def test__namespaces_from_file(self):
        ref = {"http://example.com/ns/config": '',
               "http://example.com/ns/config/val": "val"}
        xmlfile = anyconfig.compat.StringIO(XML_W_NS_S)
        self.assertTrue(dicts_equal(TT._namespaces_from_file(xmlfile), ref))


class Test_10(unittest.TestCase):

    def test_10_elem_to_container__None(self):
        self.assertEqual(TT.elem_to_container(None, dict, {}), dict())

    def test_10_root_to_container__None(self):
        self.assertEqual(TT.root_to_container(None, dict, {}), dict())

    def test_20_elem_to_container__attrs(self):
        ref = dict(a={"@attrs": dict(x='1', y='y')})
        root = TT.ET.XML("<a x='1' y='y'/>")
        self.assertEqual(TT.elem_to_container(root, dict, {}), ref)

    def test_30_elem_to_container__child(self):
        ref = dict(a=dict(b="b"))
        root = TT.ET.XML("<a><b>b</b></a>")
        self.assertEqual(TT.elem_to_container(root, dict, {}), ref)

    def test_32_elem_to_container__children(self):
        ref = {'a': {'@children': [{'b': 'b'}, {'c': 'c'}]}}
        root = TT.ET.XML("<a><b>b</b><c>c</c></a>")
        self.assertEqual(TT.elem_to_container(root, dict, {}), ref)

    def test_40_elem_to_container__text(self):
        root = TT.ET.XML("<a>A</a>")
        self.assertEqual(TT.elem_to_container(root, dict, {}), {'a': 'A'})

    def test_42_elem_to_container__text_attrs(self):
        ref = dict(a={"@attrs": {'x': 'X'}, "@text": "A"})
        root = TT.ET.XML("<a x='X'>A</a>")
        self.assertEqual(TT.elem_to_container(root, dict, {}), ref)

    def test_50_root_to_container__text_attrs_pprefix(self):
        ref = dict(a={"_attrs": {'x': 'X'}, "_text": "A"})
        root = TT.ET.XML("<a x='X'>A</a>")
        self.assertEqual(TT.root_to_container(root, dict, {}, pprefix='_'),
                         ref)


def tree_to_string(tree):
    return TT.ET.tostring(tree.getroot())


class Test_20(unittest.TestCase):

    def test_00_container_to_etree__None(self):
        self.assertTrue(TT.container_to_etree(None) is None)

    def test_10_container_to_etree__text_attrs(self):
        ref = to_bytes('<a x="X" y="Y">A</a>')
        obj = dict(a={"@attrs": {'x': 'X', 'y': 'Y'}, "@text": "A"})
        res = TT.container_to_etree(obj)
        self.assertEqual(tree_to_string(res), ref)

    def test_12_container_to_etree__text_attrs_pprefix(self):
        ref = to_bytes('<a x="X" y="Y">A</a>')
        obj = dict(a={"_attrs": {'x': 'X', 'y': 'Y'}, "_text": "A"})
        res = TT.container_to_etree(obj, pprefix='_')
        self.assertEqual(tree_to_string(res), ref)

    def test_20_container_to_etree__child(self):
        ref = to_bytes("<a><b>b</b></a>")
        obj = dict(a=dict(b="b"))
        res = TT.container_to_etree(obj)
        self.assertEqual(tree_to_string(res), ref)

    def test_22_container_to_etree__children(self):
        ref = to_bytes("<a><b>b</b><c>c</c></a>")
        obj = {'a': {'@children': [{'b': 'b'}, {'c': 'c'}]}}
        res = TT.container_to_etree(obj)
        self.assertEqual(tree_to_string(res), ref)


class Test10(anyconfig.backend.tests.ini.Test10):

    cnf = CNF_0
    cnf_s = CNF_0_S.encode("utf-8")
    load_options = dump_options = dict(pprefix='@')

    def setUp(self):
        self.psr = TT.Parser()


class Test20(anyconfig.backend.tests.ini.Test20):

    psr_cls = TT.Parser
    cnf = CNF_0
    cnf_s = CNF_0_S
    cnf_fn = "conf0.xml"

    def setUp(self):
        self.psr = self.psr_cls()
        self.workdir = anyconfig.tests.common.setup_workdir()
        self.cpath = os.path.join(self.workdir, self.cnf_fn)
        with self.psr.wopen(self.cpath) as out:
            if anyconfig.compat.IS_PYTHON_3:
                out.write(self.cnf_s.encode("utf-8"))
            else:
                out.write(self.cnf_s)

    def test_12_load__w_options(self):
        cnf = self.psr.load(self.cpath, parse_int=None)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_22_dump__w_special_option(self):
        self.psr.dump(self.cnf, self.cpath, parse_int=None, indent=3)
        cnf = self.psr.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

# vim:sw=4:ts=4:et:
