#
# Copyright (C) 2011 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Some XML modules may be missing and Base.{load,dumps}_impl are not overriden:
# pylint: disable=import-error
"""XML files parser backend, should be available always.

- Format to support: XML, e.g. http://www.w3.org/TR/xml11/
- Requirements: one of the followings

  - xml.etree.cElementTree in standard lib if python >= 2.5
  - xml.etree.ElementTree in standard lib if python >= 2.5
  - elementtree.ElementTree (otherwise)

- Development Status: 3 - Alpha
- Limitations:

  - '<prefix>attrs', '<prefix>text' and '<prefix>children' are used as special
    parameter to keep XML structure of original data. You have to cusomize
    <prefix> (default: '@') if any config parameters conflict with some of
    them.

  - Some data or structures of original XML file may be lost if make it backed
    to XML file; XML file - (anyconfig.load) -> config - (anyconfig.dump) ->
    XML file

  - XML specific features (namespace, etc.) may not be processed correctly.

- Special Options:

  - pprefix: Specify parameter prefix for attributes, text and children nodes.

History:

.. versionchanged:: 0.8.0

   - Try to make a nested dict w/o extra dict having keys of attrs, text and
     children from XML string/file as much as possible.
   - Support namespaces partially.

.. versionchanged:: 0.1.0

   - Added XML dump support.
"""
from __future__ import absolute_import
from io import BytesIO

import re
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
except ImportError:
    import elementtree.ElementTree as ET

import anyconfig.backend.base
import anyconfig.compat
import anyconfig.mdicts
import anyconfig.utils


_PREFIX = "@"

_ET_NS_RE = re.compile(r"^{(\S+)}(\S+)$")


def _iterparse(xmlfile):
    """
    Avoid bug in python 3.{2,3}. See http://bugs.python.org/issue9257.

    :param xmlfile: XML file or file-like object
    """
    try:
        return ET.iterparse(xmlfile, events=("start-ns", ))
    except TypeError:
        return ET.iterparse(xmlfile, events=(b"start-ns", ))


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
    return dict(flip(t) for _, t in _iterparse(xmlfile))


def _gen_tags(pprefix=_PREFIX):
    """
    Generate special prefixed tags.

    :param pprefix: Special parameter name prefix
    :return: A tuple of prefixed (attributes, text, children)
    """
    return tuple(pprefix + x for x in ("attrs", "text", "children"))


def _tweak_ns(tag, nspaces=None, **options):
    """
    :param tag: XML tag element
    :param nspaces: A namespaces dict, {uri: prefix} or None
    :param options: Extra keyword options

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


def _elem_strip_text(elem):
    """
    :param elem: etree elem object
    """
    if elem.text:
        elem.text = elem.text.strip()


def _dicts_have_unique_keys(dics):
    """
    :param dics: [<dict or dict-like object>], must not be [] or [{...}]
    :return: True if all keys of each dict of `dics` are unique

    # Enable the followings if to allow dics is [], [{...}]:
    # >>> all(_dicts_have_unique_keys([d]) for [d]
    # ...     in ({}, {'a': 0}, {'a': 1, 'b': 0}))
    # True
    # >>> _dicts_have_unique_keys([{}, {'a': 1}, {'b': 2, 'c': 0}])
    # True

    >>> _dicts_have_unique_keys([{}, {'a': 1}, {'a': 2}])
    False
    >>> _dicts_have_unique_keys([{}, {'a': 1}, {'b': 2}, {'b': 3, 'c': 0}])
    False
    >>> _dicts_have_unique_keys([{}, {}])
    True
    """
    key_itr = anyconfig.compat.from_iterable(d.keys() for d in dics)
    return len(set(key_itr)) == sum(len(d) for d in dics)


def _sum_dicts(dics, to_container=dict):
    """
    :param dics: [<dict/-like object must not have same keys each other>]
    :param to_container: callble to make a container object
    :return: <container> object
    """
    dic_itr = anyconfig.compat.from_iterable(d.items() for d in dics)
    return to_container(anyconfig.compat.OrderedDict(dic_itr))


def elem_to_container(elem, to_container=dict, **options):
    """
    Convert XML ElementTree Element to a collection of container objects.

    :param elem: etree elem object or None
    :param to_container: callble to make a container object
    :param options: Keyword options
        - nspaces: A namespaces dict, {uri: prefix} or None
        - tags: (attrs, text, children) parameter names
    """
    dic = to_container()
    if elem is None:
        return dic

    subdic = dic[_tweak_ns(elem.tag, **options)] = to_container()
    (attrs, text, children) = options.get("tags", _gen_tags())
    _num_of_children = len(elem)
    _elem_strip_text(elem)

    if elem.text:
        if _num_of_children or elem.attrib:
            subdic[text] = elem.text
        else:
            # .. note:: Treat as special case for later convenience.
            dic[elem.tag] = elem.text

    if elem.attrib:
        subdic[attrs] = to_container(elem.attrib)

    if _num_of_children:
        subdics = [elem_to_container(c, to_container=to_container, **options)
                   for c in elem]
        # .. note:: Another special case can omit extra <children> node.
        sdics = [subdic] + subdics
        if _dicts_have_unique_keys(sdics):
            dic[elem.tag] = _sum_dicts(sdics, to_container)
        elif not subdic:  # Only these children.
            dic[elem.tag] = subdics
        else:
            subdic[children] = subdics

    elif not elem.text and not elem.attrib:  # ex. <tag/>.
        dic[elem.tag] = None

    return dic


def root_to_container(root, to_container=dict, nspaces=None, **options):
    """
    Convert XML ElementTree Root Element to a collection of container objects.

    :param root: etree root object or None
    :param to_container: callble to make a container object
    :param nspaces: A namespaces dict, {uri: prefix} or None
    :param options: Keyword options,
        - pprefix: Special parameter name prefix
    """
    tree = to_container()
    if root is None:
        return tree

    if nspaces:
        for uri, prefix in nspaces.items():
            root.attrib["xmlns:" + prefix if prefix else "xmlns"] = uri

    if "tags" not in options:
        options["tags"] = _gen_tags(options.get("pprefix", _PREFIX))
    return elem_to_container(root, to_container=to_container, nspaces=nspaces,
                             **options)


def _elem_from_descendants(children, pprefix=_PREFIX):
    """
    :param children: A list of child dict objects
    :param pprefix: Special parameter name prefix
    """
    for child in children:  # child should be a dict-like object.
        for ckey, cval in anyconfig.compat.iteritems(child):
            celem = ET.Element(ckey)
            container_to_etree(cval, parent=celem, pprefix=pprefix)
            yield celem


def _get_or_update_parent(key, val, parent=None, pprefix=_PREFIX):
    """
    :param key: Key of current child (dict{,-like} object)
    :param val: Value of current child (dict{,-like} object or [dict{,...}])
    :param parent: XML ElementTree parent node object or None
    :param pprefix: Special parameter name prefix
    """
    elem = ET.Element(key)

    vals = val if anyconfig.utils.is_iterable(val) else [val]
    for val in vals:
        container_to_etree(val, parent=elem, pprefix=pprefix)

    if parent is None:  # 'elem' is the top level etree.
        return elem
    else:
        parent.append(elem)
        return parent


def container_to_etree(obj, parent=None, pprefix=_PREFIX):
    """
    Convert a dict-like object to XML ElementTree.

    :param obj: Container instance to convert to
    :param parent: XML ElementTree parent node object or None
    :param pprefix: Special parameter name prefix
    """
    if not anyconfig.mdicts.is_dict_like(obj):
        if parent is not None and obj:
            parent.text = obj  # Parent is a leaf text node.
        return  # All attributes and text should be set already.

    (attrs, text, children) = _gen_tags(pprefix)
    for key, val in anyconfig.compat.iteritems(obj):
        if key == attrs:
            for attr, aval in anyconfig.compat.iteritems(val):
                parent.set(attr, aval)
        elif key == text:
            parent.text = val
        elif key == children:
            for celem in _elem_from_descendants(val, pprefix=pprefix):
                parent.append(celem)
        else:
            parent = _get_or_update_parent(key, val, parent=parent,
                                           pprefix=pprefix)

    return ET.ElementTree(parent)


def etree_write(tree, stream):
    """
    Write XML ElementTree `root` content into `stream`.

    .. note:
       It seems that ET.ElementTree.write() cannot process a parameter
       'xml_declaration' in python 2.6.

    :param tree: XML ElementTree object
    :param stream: File or file-like object can write to
    """
    if anyconfig.compat.IS_PYTHON_2_6:
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
    _load_opts = _dump_opts = ["pprefix"]

    def load_from_string(self, content, to_container, **opts):
        """
        Load config from XML snippet (a string `content`).

        :param content:
            XML snippet string of str (python 2) or bytes (python 3) type
        :param to_container: callble to make a container object
        :param opts: optional keyword parameters passed to

        :return: Dict-like object holding config parameters
        """
        root = ET.fromstring(content)
        if anyconfig.compat.IS_PYTHON_3:
            stream = BytesIO(content)
        else:
            stream = anyconfig.compat.StringIO(content)
        nspaces = _namespaces_from_file(stream)
        return root_to_container(root, to_container=to_container,
                                 nspaces=nspaces, **opts)

    def load_from_path(self, filepath, to_container, **opts):
        """
        :param filepath: XML file path
        :param to_container: callble to make a container object
        :param opts: optional keyword parameters to be sanitized

        :return: Dict-like object holding config parameters
        """
        root = ET.parse(filepath).getroot()
        nspaces = _namespaces_from_file(filepath)
        return root_to_container(root, to_container=to_container,
                                 nspaces=nspaces, **opts)

    def load_from_stream(self, stream, to_container, **opts):
        """
        :param stream: XML file or file-like object
        :param to_container: callble to make a container object
        :param opts: optional keyword parameters to be sanitized

        :return: Dict-like object holding config parameters
        """
        root = ET.parse(stream).getroot()
        path = anyconfig.utils.get_path_from_stream(stream)
        nspaces = _namespaces_from_file(path)
        return root_to_container(root, to_container=to_container,
                                 nspaces=nspaces, **opts)

    def dump_to_string(self, cnf, **opts):
        """
        :param cnf: Configuration data to dump
        :param opts: optional keyword parameters

        :return: string represents the configuration
        """
        tree = container_to_etree(cnf, **opts)
        buf = BytesIO()
        etree_write(tree, buf)
        return buf.getvalue()

    def dump_to_stream(self, cnf, stream, **opts):
        """
        :param cnf: Configuration data to dump
        :param stream: Config file or file like object write to
        :param opts: optional keyword parameters
        """
        tree = container_to_etree(cnf, **opts)
        etree_write(tree, stream)

# vim:sw=4:ts=4:et:
