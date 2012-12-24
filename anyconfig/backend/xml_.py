#
# Copyright (C) 2011, 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.base as Base
import anyconfig.Bunch as B

import logging


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


def etree_to_Bunch(root):
    """
    Convert XML ElementTree to a collection of Bunch objects.
    """
    tree = B.Bunch()

    if len(root):  # It has children.
        # FIXME: Configuration item cannot have both attributes and
        # values (list) at the same time in current implementation:
        tree[root.tag] = [etree_to_Bunch(c) for c in root]
    else:
        tree[root.tag] = B.Bunch(**root.attrib)

    return tree


class XmlConfigParser(Base.BaseConfigParser):

    _type = "xml"
    _extensions = ["xml"]

    @classmethod
    def load(cls, config_path, *args, **kwargs):
        tree = etree.parse(config_path)
        root = tree.getroot()

        return etree_to_Bunch(root)

    @classmethod
    def dumps(cls, data, config_path, *args, **kwargs):
        raise NotImplementedError("Not yet")


# vim:sw=4:ts=4:et:
