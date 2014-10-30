#
# Copyright (C) 2011 - 2014 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=R0921
from anyconfig.globals import LOGGER as logging

import anyconfig.backend.base as Base
import anyconfig.compat as AC


SUPPORTED = True
try:
    # First, try lxml which is compatible with elementtree and looks faster a
    # lot. See also: http://getpython3.com/diveintopython3/xml.html
    from lxml2 import etree
except ImportError:
    try:
        import xml.etree.ElementTree as etree
    except ImportError:
        try:
            import elementtree.ElementTree as etree
        except ImportError:
            logging.warn("ElementTree module is not available. Disabled "
                         "XML support.")
            SUPPORTED = False


if SUPPORTED:
    def etree_getroot_fromstring(s):
        """
        :param s: A XML string
        :return: etree object gotten by parsing ``s``
        """
        return etree.ElementTree(etree.fromstring(s)).getroot()

    def etree_getroot_fromsrc(src):
        """
        :param src: A file name/path or a file[-like] object or a URL
        :return: etree object gotten by parsing ``s``
        """
        return etree.parse(src).getroot()
else:
    def _dummy_fun(*args, **kwargs):
        logging.warn("Return None as XML module is not available: "
                     "args=%s, kwargs=%s", ','.join(args), str(kwargs))
        return None

    etree_getroot_fromstring = etree_getroot_fromsrc = _dummy_fun


def etree_to_container(root, container):
    """
    Convert XML ElementTree to a collection of container objects.

    :param root: etree root object or None
    :param container: A nested dict like objects
    """
    tree = container()
    if root is None:
        return tree

    tree[root.tag] = container()

    if root.attrib:
        tree[root.tag]["attrs"] = container(AC.iteritems(root.attrib))

    if root.text and root.text.strip():
        tree[root.tag]["text"] = root.text.strip()

    if len(root):  # It has children.
        # FIXME: Configuration item cannot have both attributes and
        # values (list) at the same time in current implementation:
        tree[root.tag]["children"] = [etree_to_container(c, container) for c
                                      in root]

    return tree


class XmlConfigParser(Base.ConfigParser):

    _type = "xml"
    _extensions = ["xml"]
    _supported = SUPPORTED

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
