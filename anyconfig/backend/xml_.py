#
# Copyright (C) 2011 - 2014 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
from anyconfig.globals import LOGGER as logging
import anyconfig.backend.base as Base


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
        return etree.ElementTree(etree.fromstring(s)).getroot()

    def etree_getroot_fromfile(f):
        return etree.parse(f).getroot()
else:
    def _dummy_fun(*args, **kwargs):
        logging.warn("Return {} as no any XML modules are not "
                     "available.")
        return {}

    etree_getroot_fromstring = etree_getroot_fromfile = _dummy_fun


def etree_to_container(root, container):
    """
    Convert XML ElementTree to a collection of container objects.
    """
    tree = container()

    if len(root):  # It has children.
        # FIXME: Configuration item cannot have both attributes and
        # values (list) at the same time in current implementation:
        tree[root.tag] = container()
        tree[root.tag]["children"] = [etree_to_container(c, container) for c
                                      in root]
        tree[root.tag]["attributes"] = container(**root.attrib)

        if root.text.strip():
            tree[root.tag]["text"] = root.text.strip()
    else:
        tree[root.tag]["attributes"] = container(**root.attrib)
        if root.text.strip():
            tree[root.tag]["text"] = root.text.strip()

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
        root = etree_getroot_fromfile(config_path)
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
