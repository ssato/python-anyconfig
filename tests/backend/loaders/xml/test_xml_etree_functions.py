#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports,protected-access
# pylint: disable=too-many-arguments
#
import collections

import pytest

import anyconfig.backend.xml.etree as TT


XML_WITH_NS_0 = """<a xmlns="http://example.com/ns/config"
   xmlns:val="http://example.com/ns/config/val">
   <b>1</b>
   <val:c>C</val:c>
</a>
"""

CNF_0 = {'config': {'@attrs': {'val:name': 'foo',
                               'xmlns': 'http://example.com/ns/cnf',
                               'xmlns:val': 'http://example.com/ns/cnf/val'},
                    'val:a': '0',
                    'val:b': {'@attrs': {'id': 'b0'}, '@text': 'bbb'},
                    'val:c': None,
                    'sect0': {'val:d': 'x, y, z'},
                    'list1': [{'item': '0'}, {'item': '1'}, {'item': '2'}],
                    'list2': {'@attrs': {'id': 'list2'},
                              '@children': [{'item': 'i'},
                                            {'item': 'j'}]}}}


def to_bytes(astr):
    """Convert a string to bytes.
    """
    return bytes(astr, 'utf-8')


def to_xml_elem(astr: str) -> TT.ElementTree.Element:
    """Convert a string to XML element object."""
    return TT.ElementTree.fromstring(astr)


@pytest.mark.parametrize(
    ("path", "exp"),
    (("tests/res/1/loaders/xml.etree/10/100.xml", {}),
     ("tests/res/1/loaders/xml.etree/10/200.xml",
      {"http://example.com/ns/config": "",
       "http://example.com/ns/config/val": "val"}),
     ),
)
def test__namespaces_from_file(path: str, exp):
    assert TT._namespaces_from_file(path) == exp


@pytest.mark.parametrize(
    ("tag", "nspaces", "exp"),
    (("a", {}, "a"),
     ("a", {"http://example.com/ns/val/": "val"}, "a"),
     ("{http://example.com/ns/val/}a",
      {"http://example.com/ns/val/": "val"},
      "val:a"),
     ),
)
def test__tweak_ns(tag, nspaces, exp):
    assert TT._tweak_ns(tag, nspaces=nspaces) == exp


@pytest.mark.parametrize(
    ("dics", "exp"),
    ((({}, {"a": 1}, {"a": 2}), False),
     (({"a": 1}, {"b": 2}, {"b": 3, "c": 0}), False),
     (({}, {}), True),
     (({"(": 1}, {"b": 2}, {"c": 0}), True),
     ),
)
def test__dicts_have_unique_keys(dics, exp):
    assert TT._dicts_have_unique_keys(dics) == exp


@pytest.mark.parametrize(
    ("val", "opts", "exp"),
    (("1", {}, "1"),
     ("1", {"ac_parse_value": True}, 1),
     ),
)
def test__parse_text_parse_text(val, opts, exp):
    assert TT._parse_text(val, **opts) == exp


@pytest.mark.parametrize(
    ("elem_s", "opts", "exp_elem_text", "exp_dic", "exp_subdic"),
    (("<a> </a>", {}, "", {}, {}),
     ("<a> </a>", {"text": "#text"}, "", {}, {}),
     ("<p:a xmlns:p='http://example.com'> </p:a>", {}, "", {}, {}),
     ("<a>1</a>", {}, "1", {"a": "1"}, {}),
     ("<a>1</a>", {"ac_parse_value": True}, "1", {"a": 1}, {}),
     ("<a id='1'>1</a>", {"text": "#text"}, "1", {}, {"#text": "1"}),
     ("<a id='1'>1</a>", {"text": "#text", "ac_parse_value": True},
      "1", {}, {"#text": 1}),
     ("<a>1<b/></a>", {}, "1", {}, {"@text": "1"}),
     ("<a id='A' />", {}, None, {}, {}),
     ),
)
def test__process_elem_text(elem_s, opts, exp_elem_text, exp_dic, exp_subdic):
    (elem, dic, subdic) = (to_xml_elem(elem_s), {}, {})
    TT._process_elem_text(elem, dic, subdic, **opts)

    assert elem.text == exp_elem_text
    assert dic == exp_dic
    assert subdic == exp_subdic


@pytest.mark.parametrize(
    ("elem_s", "opts", "exp_dic", "exp_subdic"),
    (("<a id='A'/>", {}, {}, {"@attrs": {"id": "A"}}),
     ("<a id='A'>AAA</a>", {}, {}, {"@attrs": {"id": "A"}}),
     ("<a id='A'/>", {"merge_attrs": True}, {"a": {"id": "A"}}, {}),
     ("<a id='1'/>", {"ac_parse_value": True}, {}, {"@attrs": {"id": 1}}),
     ("<a id='A'/>", {"ac_parse_value": True}, {}, {"@attrs": {"id": "A"}}),
     ("<a id='true'/>", {"ac_parse_value": True}, {},
      {"@attrs": {"id": True}}),
     ),
)
def test__process_elem_attrs(elem_s, opts, exp_dic, exp_subdic):
    (elem, dic, subdic) = (to_xml_elem(elem_s), {}, {})
    TT._process_elem_attrs(elem, dic, subdic, **opts)

    assert dic == exp_dic
    assert subdic == exp_subdic


@pytest.mark.parametrize(
    ("elem_s", "opts", "exp_dic", "exp_subdic"),
    (("<a><x>X</x><y>Y</y></a>", {}, {"a": {"x": "X", "y": "Y"}}, {}),
     ("<list><i>A</i><i>B</i></list>", {},
      {"list": [{"i": "A"}, {"i": "B"}]}, {}),
     ("<list id='xyz'><i>A</i><i>B</i></list>", {"children": "#children"},
      {"list": [{"i": "A"}, {"i": "B"}]}, {}),
     ("<a z='Z'><x>X</x><y>Y</y></a>", {"merge_attrs": True},
      {"a": {"x": "X", "y": "Y", "z": "Z"}}, {}),
     ),
)
def test_process_children_elems(
    elem_s, opts, exp_dic, exp_subdic
):
    (elem, dic, subdic) = (to_xml_elem(elem_s), {}, {})
    TT._process_children_elems(elem, dic, subdic, **opts)

    assert dic == exp_dic
    assert subdic == exp_subdic


def test_elem_to_container__none():
    assert TT.elem_to_container(None) == {}
    assert TT.elem_to_container(
        None, container=collections.OrderedDict
    ) == collections.OrderedDict()


_E2C_DATASETS = _R2C_DATASETS = (
    ("<a/>", {"a": None}),
    ("<a>A</a>", {"a": "A"}),
    ("<a x='X'>A</a>",
     {"a": {"@attrs": {"x": "X"}, "@text": "A"}}),
    ("<a><b>b</b></a>", {"a": {"b": "b"}}),
    ("<a><b>1</b><b>2</b></a>",
     {"a": [{"b": "1"}, {"b": "2"}]}),
    ("<a><b>b</b><c>c</c></a>",
     {'a': {'b': 'b', 'c': 'c'}}),
    ("<a x='1' y='y'/>",
     {"a": {"@attrs": {"x": "1", "y": "y"}}}),
    ("<a>aaa<b>1</b><b>2</b></a>",
     {"a": {"@text": "aaa", "@children": [{"b": "1"}, {"b": "2"}]}}),
)


@pytest.mark.parametrize(("elem_s", "exp"), _E2C_DATASETS)
def test_elem_to_container(elem_s, exp):
    assert TT.elem_to_container(
        to_xml_elem(elem_s)
    ) == exp


def test_root_to_container__none():
    assert TT.root_to_container(None) == {}
    assert TT.root_to_container(
        None, container=collections.OrderedDict
    ) == collections.OrderedDict()


@pytest.mark.parametrize(("root_s", "exp"), _R2C_DATASETS)
def test_root_to_container(root_s: str, exp):
    assert TT.root_to_container(
        to_xml_elem(root_s)
    ) == exp


@pytest.mark.parametrize(
    ("obj", "parent"),
    ((None, None),
     ({}, None),
     ),
)
def test_container_to_elem__errors(obj, parent):
    with pytest.raises(ValueError):
        assert TT.container_to_elem(obj, parent=parent)


@pytest.mark.parametrize(
    ("obj", "exp_s"),
    (({"a": {"@attrs": {'x': 'X', 'y': 'Y'}, "@text": "A"}},
      '<a x="X" y="Y">A</a>'),
     ({"a": {"b": "b"}},
      "<a><b>b</b></a>"),
     ({'a': {'@children': [{'b': 'b'}, {'c': 'c'}]}},
      "<a><b>b</b><c>c</c></a>"),
     ),
)
def test_container_to_elem(obj, exp_s):
    assert TT.ElementTree.tostring(
        TT.container_to_elem(obj)
    ) == to_bytes(exp_s)


@pytest.mark.parametrize(
    ("obj", "tags", "exp_s"),
    (({"a": {"_attrs": {'x': 'X', 'y': 'Y'}, "_text": "A"}},
      {"attrs": "_attrs", "text": "_text"},
      '<a x="X" y="Y">A</a>'),
     ),
)
def test_container_to_elem_with_tags(obj, tags, exp_s):
    assert TT.ElementTree.tostring(
        TT.container_to_elem(obj, tags=tags)
    ) == to_bytes(exp_s)
