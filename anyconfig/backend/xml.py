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


def etree_to_container(root, cls):
    """
    Convert XML ElementTree to a collection of container objects.

    :param root: etree root object or None
    :param cls: Container class
    """
    tree = cls()
    if root is None:
        return tree

    tree[root.tag] = cls()

    if root.attrib:
        tree[root.tag]["attrs"] = cls(anyconfig.compat.iteritems(root.attrib))

    if root.text and root.text.strip():
        tree[root.tag]["text"] = root.text.strip()

    if len(root):  # It has children.
        # Note: Configuration item cannot have both attributes and values
        # (list) at the same time in current implementation:
        tree[root.tag]["children"] = [etree_to_container(c, cls) for c in root]

    return tree


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
    def dumps_impl(cls, data, **kwargs):
        """
        :param data: Data to dump :: dict
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: string represents the configuration
        """
        raise NotImplementedError("XML dumper not implemented yet!")

# vim:sw=4:ts=4:et:
