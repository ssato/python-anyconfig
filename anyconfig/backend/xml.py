#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Some of XML backend modules may be missing:
# pylint: disable=import-error
"""XML files parser backend, should be available always.

- Format to support: XML, e.g. http://www.w3.org/TR/xml11/
- Requirements: one of the followings

  - lxml2.etree if available
  - xml.etree.ElementTree in standard lib if python >= 2.5
  - elementtree.ElementTree (otherwise)

- Limitations:

  - 'attrs', 'text' and 'children' are used as special keyword to keep XML
    structure of config data so that these are not allowed to used in config
    files.

  - Some data or structures of original XML file may be lost if make it backed
    to XML file; XML file - (anyconfig.load) -> config - (anyconfig.dump) ->
    XML file

- Special Options: None supported
"""
from __future__ import absolute_import

import anyconfig.backend.base
import anyconfig.compat

try:
    # First, try lxml which is compatible with elementtree and looks faster a
    # lot. See also: http://getpython3.com/diveintopython3/xml.html
    from lxml2 import etree as ET
except ImportError:
    try:
        import xml.etree.ElementTree as ET
    except ImportError:
        import elementtree.ElementTree as ET


def etree_getroot_fromstring(str_):
    """
    :param s: A XML string
    :return: etree object gotten by parsing `str_`
    """
    return ET.ElementTree(ET.fromstring(str_)).getroot()


def etree_getroot_fromsrc(src):
    """
    :param src: A file name/path or a file[-like] object or a URL
    :return: etree object gotten by parsing ``s``
    """
    return ET.parse(src).getroot()


def etree_to_container(root, cls, attrs="@attrs", text="@text",
                       children="@children"):
    """
    Convert XML ElementTree to a collection of container objects.

    :param root: etree root object or None
    :param cls: Container class
    :param attrs: Key name for XML attributes
    :param text: Key name for XML text elements
    :param children: Key name for XML child elements
    """
    tree = cls()
    if root is None:
        return tree

    tree[root.tag] = cls()

    if root.attrib:
        tree[root.tag][attrs] = cls(anyconfig.compat.iteritems(root.attrib))

    if root.text and root.text.strip():
        tree[root.tag][text] = root.text.strip()

    if len(root):  # It has children.
        # Note: Configuration item cannot have both attributes and values
        # (list) at the same time in current implementation:
        tree[root.tag][children] = [etree_to_container(c, cls, attrs, text,
                                                       children) for c in root]

    return tree


def container_to_etree(obj, cls, parent=None, attrs="@attrs", text="@text",
                       children="@children"):
    """
    Convert a container object to XML ElementTree.

    :param obj: Container instance to convert to
    :param cls: Container class
    :param parent: XML ElementTree parent node object or None
    :param attrs: Key name for XML attributes
    :param text: Key name for XML text elements
    :param children: Key name for XML child elements

    >>> obj = {'config': {'@attrs': {'name': 'foo'},
    ...                   '@children': [{'a': {'@text': '0'}},
    ...                                 {'b': {'@attrs': {'id': 'b0'},
    ...                                        '@text': 'bbb'}}]}}
    >>> tree = container_to_etree(obj, Parser.container())
    >>> buf = anyconfig.compat.StringIO()
    >>> tree.write(buf)
    >>> buf.getvalue()
    '<config name="foo"><a>0</a><b id="b0">bbb</b></config>'
    >>>
    """
    if not isinstance(obj, (cls, dict)):
        return  # All attributes and text should be set already.

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
                    container_to_etree(cval, cls, celem, attrs, text, children)
                    parent.append(celem)
        else:
            elem = ET.Element(key)
            container_to_etree(val, cls, elem, attrs, text, children)
            return ET.ElementTree(elem)


class Parser(anyconfig.backend.base.Parser):
    """
    Parser for XML files.
    """
    _type = "xml"
    _extensions = ["xml"]

    @classmethod
    def loads(cls, config_content, **kwargs):
        """
        :param config_content:  Config file content
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: cls.container() object holding config parameters
        """
        root = etree_getroot_fromstring(config_content)
        return etree_to_container(root, cls.container())

    @classmethod
    def load(cls, config_path, **kwargs):
        """
        :param config_path:  Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: cls.container() object holding config parameters
        """
        root = etree_getroot_fromsrc(config_path)
        return etree_to_container(root, cls.container())

    @classmethod
    def dumps(cls, obj, **kwargs):
        """
        :param obj: Data to dump :: dict
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: string represents the configuration
        """
        root = container_to_etree(obj, cls.container())
        buf = anyconfig.compat.StringIO()
        root.write(buf, encoding='UTF-8', xml_declaration=True)
        return buf.getvalue()

    @classmethod
    def dump_impl(cls, obj, config_path, **kwargs):
        """
        :param obj: Data to dump :: dict
        :param config_path: Dump destination file path
        :param kwargs: backend-specific optional keyword parameters :: dict
        """
        root = container_to_etree(obj, cls.container())
        with open(config_path, cls._open_flags[1]) as out:
            root.write(out, encoding='UTF-8', xml_declaration=True)

# vim:sw=4:ts=4:et:
