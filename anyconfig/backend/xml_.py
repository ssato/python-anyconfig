#
# Copyright (C) 2011, 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
from anyconfig.globals import LOGGER as logging
import anyconfig.backend.base as Base


SUPPORTED = True
try:
    # First, try lxml compatible with elementtree and looks faster a lot.
    # see also: http://diveintopython3-ja.rdy.jp/xml.html:
    from lxml import etree
except ImportError:
    try:
        import xml.etree.ElementTree as etree
    except ImportError:
        try:
            import elementtree.ElementTree as etree
        except ImportError:
            logging.warn(
                "ElementTree module is not available. Disabled XML support."
            )
            SUPPORTED = False


def etree_to_container(root, container):
    """
    Convert XML ElementTree to a collection of container objects.
    """
    tree = container()

    if len(root):  # It has children.
        # FIXME: Configuration item cannot have both attributes and
        # values (list) at the same time in current implementation:
        tree[root.tag] = [etree_to_container(c, container) for c in root]
    else:
        tree[root.tag] = container(**root.attrib)

    return tree


if SUPPORTED:
    def etree_getroot_fromstring(s):
        return etree.fromstring(s).getroot()

    def etree_getroot_fromfile(f):
        return etree.parse(f).getroot()
else:
    def _dummy_fun(*args, **kwargs):
        logging.warn(
            "Return {} as no any XML modules used, are not available."
        )
        return {}

    etree_getroot_fromstring = etree_getroot_fromfile = _dummy_fun


class XmlConfigParser(Base.ConfigParser):

    _type = "xml"
    _extensions = ["xml"]
    _supported = SUPPORTED

    @classmethod
    def loads(cls, config_content, *args, **kwargs):
        root = etree_getroot_fromstring(config_content)
        return etree_to_container(root, cls.container())

    @classmethod
    def load(cls, config_path, *args, **kwargs):
        root = etree_getroot_fromfile(config_path)
        return etree_to_container(root, cls.container())

# vim:sw=4:ts=4:et:
