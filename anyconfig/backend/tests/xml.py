#
# Copyright (C) 2012 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, protected-access
from __future__ import absolute_import
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


class Test_00(unittest.TestCase):

    def test__namespaces_from_file(self):
        ref = {"http://example.com/ns/config": '',
               "http://example.com/ns/config/val": "val"}
        xmlfile = anyconfig.compat.StringIO(XML_W_NS_S)
        self.assertTrue(dicts_equal(TT._namespaces_from_file(xmlfile), ref))


class Test_10(unittest.TestCase):

    def test_elem_to_container__None(self):
        self.assertEqual(TT.elem_to_container(None, dict, {}), dict())

    def test_root_to_container__None(self):
        self.assertEqual(TT.root_to_container(None, dict, {}), dict())

    def test_elem_to_container__attrs(self):
        ref = dict(a={"@attrs": dict(x='1', y='y')})
        root = TT.ET.XML("<a x='1' y='y'/>")
        self.assertEqual(TT.elem_to_container(root, dict, {}), ref)

    def test_elem_to_container__child(self):
        ref = dict(a=dict(b="b"))
        root = TT.ET.XML("<a><b>b</b></a>")
        self.assertEqual(TT.elem_to_container(root, dict, {}), ref)

    def test_elem_to_container__children(self):
        ref = {'a': {'@children': [{'b': 'b'}, {'c': 'c'}]}}
        root = TT.ET.XML("<a><b>b</b><c>c</c></a>")
        self.assertEqual(TT.elem_to_container(root, dict, {}), ref)

    def test_elem_to_container__text(self):
        root = TT.ET.XML("<a>A</a>")
        self.assertEqual(TT.elem_to_container(root, dict, {}), {'a': 'A'})

    def test_elem_to_container__text_attrs(self):
        ref = dict(a={"@attrs": {'x': 'X'}, "@text": "A"})
        root = TT.ET.XML("<a x='X'>A</a>")
        self.assertEqual(TT.elem_to_container(root, dict, {}), ref)


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

# vim:sw=4:ts=4:et:
