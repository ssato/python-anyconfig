#
# Copyright (C) 2011 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Some XML modules may be missing and Base.{load,dumps}_impl are not overriden:
# pylint: disable=import-error
"""XML files parser backend, should be available always.

.. versionchanged:: 0.1.0
   Added XML dump support.

- Format to support: XML, e.g. http://www.w3.org/TR/xml11/
- Requirements: one of the followings

  - lxml2.etree if available
  - xml.etree.ElementTree in standard lib if python >= 2.5
  - elementtree.ElementTree (otherwise)

- Limitations:

  - '<prefix>attrs', '<prefix>text' and '<prefix>children' are used as special
    parameter to keep XML structure of original data. You have to cusomize
    <prefix> (default: '@') if any config parameters conflict with some of
    them.

  - Some data or structures of original XML file may be lost if make it backed
    to XML file; XML file - (anyconfig.load) -> config - (anyconfig.dump) ->
    XML file

  - XML specific features (namespace, etc.) may not be processed correctly.

- Special Options: None supported
"""
from __future__ import absolute_import
from io import BytesIO

import re
import sys
try:
    # First, try lxml which is compatible with elementtree and looks faster a
    # lot. See also: http://getpython3.com/diveintopython3/xml.html
    from lxml2 import etree as ET
except ImportError:
    try:
        import xml.etree.ElementTree as ET
    except ImportError:
        import elementtree.ElementTree as ET

import anyconfig.backend.base
import anyconfig.compat
import anyconfig.mdicts


_PREFIX = "@"

# It seems that ET.ElementTree.write() cannot process a parameter
# 'xml_declaration' in older python < 2.7:
_IS_OLDER_PYTHON = sys.version_info[0] < 3 and sys.version_info[1] < 7

_ET_NS_RE = re.compile(r"^{(\S+)}(\S+)$")


def flip(tpl):
    """
    >>> flip((1, 2))
    (2, 1)
    """
    return (tpl[1], tpl[0])


def _namespaces_from_file(xmlfile):
    """
    :param xmlfile: XML file or file-like object
    :return: {namespace_uri: namespace_prefix} or {}
    """
    return dict(flip(t) for _, t
                in ET.iterparse(xmlfile, events=["start-ns"]))


def _gen_tags(pprefix=_PREFIX):
    """
    Generate special prefixed tags.

    :param pprefix: Special parameter name prefix
    :return: A tuple of prefixed (attributes, text, children)
    """
    return tuple(pprefix + x for x in ("attrs", "text", "children"))


def _tweak_ns(tag, nspaces):
    """
    :param tag: XML tag element
    :param nspaces: A namespaces dict, {uri: prefix}

    >>> _tweak_ns("a", {})
    'a'
    >>> _tweak_ns("a", {"http://example.com/ns/val/": "val"})
    'a'
    >>> _tweak_ns("{http://example.com/ns/val/}a",
    ...           {"http://example.com/ns/val/": "val"})
    'val:a'
    """
    if nspaces:
        matched = _ET_NS_RE.match(tag)
        if matched:
            (uri, tag) = matched.groups()
            prefix = nspaces.get(uri, False)
            if prefix:
                return "%s:%s" % (prefix, tag)

    return tag


def root_to_container(root, to_container, nspaces, pprefix=_PREFIX):
    """
    Convert XML ElementTree Root Element to a collection of container objects.

    :param root: etree root object or None
    :param to_container: callble to make a container object
    :param nspaces: A namespaces dict, {uri: prefix}
    :param pprefix: Special parameter name prefix
    """
    tree = to_container()
    if root is None:
        return tree

    if nspaces is None:
        nspaces = dict()

    if nspaces:
        for uri, prefix in nspaces.items():
            root.attrib["xmlns:" + prefix if prefix else "xmlns"] = uri

    return elem_to_container(root, to_container, nspaces, _gen_tags(pprefix))


def elem_to_container(elem, to_container, nspaces, tags=False):
    """
    Convert XML ElementTree Element to a collection of container objects.

    :param elem: etree elem object or None
    :param to_container: callble to make a container object
    :param nspaces: A namespaces dict, {uri: prefix}
    :param tags: (attrs, text, children) parameter names
    """
    tree = to_container()
    if elem is None:
        return tree

    subtree = tree[_tweak_ns(elem.tag, nspaces)] = to_container()
    (attrs, text, children) = tags if tags else _gen_tags()
    _num_of_children = len(elem)

    if elem.attrib:
        subtree[attrs] = to_container(elem.attrib)

    if elem.text:
        elem.text = elem.text.strip()
        if elem.text:
            if not _num_of_children and not elem.attrib:
                # .. note:: Treat as special case for later convenience.
                tree[elem.tag] = elem.text
            else:
                subtree[text] = elem.text

    if _num_of_children:
        # Note: Configuration item cannot have both attributes and values
        # (list) at the same time in current implementation:
        args = (to_container, nspaces, tags)
        if _num_of_children == 1:  # .. note:: Another special case.
            tree[elem.tag] = [elem_to_container(c, *args) for c in elem][0]
        else:
            subtree[children] = [elem_to_container(c, *args) for c in elem]

    return tree


def container_to_etree(obj, parent=None, pprefix=_PREFIX):
    """
    Convert a dict-like object to XML ElementTree.

    :param obj: Container instance to convert to
    :param parent: XML ElementTree parent node object or None
    :param pprefix: Special parameter name prefix
    """
    if not anyconfig.mdicts.is_dict_like(obj):
        return  # All attributes and text should be set already.

    (attrs, text, children) = _gen_tags(pprefix)
    _has_attr_or_child = any(k in (attrs, children) for k in obj.keys())

    for key, val in anyconfig.compat.iteritems(obj):
        if key == attrs:
            for attr, aval in anyconfig.compat.iteritems(val):
                parent.set(attr, aval)
        elif key == text or _has_attr_or_child:
            parent.text = val
        elif key == children:
            for child in val:  # child should be a dict-like object.
                for ckey, cval in anyconfig.compat.iteritems(child):
                    celem = ET.Element(ckey)
                    container_to_etree(cval, celem, pprefix)
                    parent.append(celem)
        else:
            elem = ET.Element(key)
            container_to_etree(val, elem, pprefix)
            return ET.ElementTree(elem)


def etree_write(tree, stream):
    """
    Write XML ElementTree `root` content into `stream`.

    :param tree: XML ElementTree object
    :param stream: File or file-like object can write to
    """
    if _IS_OLDER_PYTHON:
        tree.write(stream, encoding='UTF-8')
    else:
        tree.write(stream, encoding='UTF-8', xml_declaration=True)


class Parser(anyconfig.backend.base.ToStreamDumper):
    """
    Parser for XML files.
    """
    _type = "xml"
    _extensions = ["xml"]
    _open_flags = ('rb', 'wb')

    def load_from_string(self, content, to_container, **kwargs):
        """
        Load config from XML snippet (a string `content`).

        :param content: XML snippet (a string)
        :param to_container: callble to make a container object
        :param kwargs: optional keyword parameters passed to

        :return: Dict-like object holding config parameters
        """
        root = ET.fromstring(content)
        nspaces = _namespaces_from_file(anyconfig.compat.StringIO(content))
        return root_to_container(root, to_container, nspaces)

    def load_from_path(self, filepath, to_container, **kwargs):
        """
        :param filepath: XML file path
        :param to_container: callble to make a container object
        :param kwargs: optional keyword parameters to be sanitized

        :return: Dict-like object holding config parameters
        """
        root = ET.parse(filepath).getroot()
        nspaces = _namespaces_from_file(filepath)
        return root_to_container(root, to_container, nspaces)

    def load_from_stream(self, stream, to_container, **kwargs):
        """
        :param stream: XML file or file-like object
        :param to_container: callble to make a container object
        :param kwargs: optional keyword parameters to be sanitized

        :return: Dict-like object holding config parameters
        """
        return self.load_from_path(stream, to_container, **kwargs)

    def dump_to_string(self, cnf, **kwargs):
        """
        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters

        :return: string represents the configuration
        """
        tree = container_to_etree(cnf)
        buf = BytesIO()
        etree_write(tree, buf)
        return buf.getvalue()

    def dump_to_stream(self, cnf, stream, **kwargs):
        """
        :param cnf: Configuration data to dump
        :param stream: Config file or file like object write to
        :param kwargs: optional keyword parameters
        """
        tree = container_to_etree(cnf)
        etree_write(tree, stream)

# vim:sw=4:ts=4:et:
