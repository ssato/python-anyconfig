#
# Copyright (C) 2011 - 2016 Satoru SATOH <ssato @ redhat.com>
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

import sys

import anyconfig.backend.base
import anyconfig.compat
import anyconfig.mdicts

try:
    # First, try lxml which is compatible with elementtree and looks faster a
    # lot. See also: http://getpython3.com/diveintopython3/xml.html
    from lxml2 import etree as ET
except ImportError:
    try:
        import xml.etree.ElementTree as ET
    except ImportError:
        import elementtree.ElementTree as ET


_PARAM_PREFIX = "@"

# It seems that ET.ElementTree.write() cannot process a parameter
# 'xml_declaration' in older python < 2.7:
_IS_OLDER_PYTHON = sys.version_info[0] < 3 and sys.version_info[1] < 7


def _gen_tags(pprefix=_PARAM_PREFIX):
    """
    Generate special prefixed tags.

    :param pprefix: Special parameter name prefix
    :return: A tuple of tags (attributes, text, children)
    """
    return (pprefix + x for x in ("attrs", "text", "children"))


def etree_to_container(root, cls, pprefix=_PARAM_PREFIX):
    """
    Convert XML ElementTree to a collection of container objects.

    :param root: etree root object or None
    :param cls: Container class
    :param pprefix: Special parameter name prefix
    """
    (attrs, text, children) = _gen_tags(pprefix)
    tree = cls()
    if root is None:
        return tree

    tree[root.tag] = cls()

    if root.attrib:
        tree[root.tag][attrs] = cls(root.attrib)

    if root.text and root.text.strip():
        tree[root.tag][text] = root.text.strip()

    if len(root):  # It has children.
        # Note: Configuration item cannot have both attributes and values
        # (list) at the same time in current implementation:
        tree[root.tag][children] = [etree_to_container(c, cls, pprefix)
                                    for c in root]

    return tree


def container_to_etree(obj, parent=None, pprefix=_PARAM_PREFIX):
    """
    Convert a dict-like object to XML ElementTree.

    :param obj: Container instance to convert to
    :param parent: XML ElementTree parent node object or None
    :param pprefix: Special parameter name prefix
    """
    if not anyconfig.mdicts.is_dict_like(obj):
        return  # All attributes and text should be set already.

    (attrs, text, children) = _gen_tags(pprefix)
    for key, val in anyconfig.compat.iteritems(obj):
        if key == attrs:
            for attr, aval in anyconfig.compat.iteritems(val):
                parent.set(attr, aval)
        elif key == text:
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
        root = ET.ElementTree(ET.fromstring(content)).getroot()
        return etree_to_container(root, to_container)

    def load_from_path(self, filepath, to_container, **kwargs):
        """
        :param filepath: XML file path
        :param to_container: callble to make a container object
        :param kwargs: optional keyword parameters to be sanitized

        :return: Dict-like object holding config parameters
        """
        root = ET.parse(filepath).getroot()
        return etree_to_container(root, to_container)

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
