#
# Copyright (C) 2017 Red Hat, Inc.
# License: MIT
#
"""Flatten nested dicts, etc.
"""
from __future__ import absolute_import

import itertools
import operator

import m9dicts.compat
import m9dicts.utils


def object_to_id(obj):
    """Object -> id.

    :param obj: Any object has __str__ method to get its ID value

    >>> object_to_id("test")
    '098f6bcd4621d373cade4e832627b4f6'
    >>> object_to_id({'a': "test"})
    'c5b846ec3b2f1a5b7c44c91678a61f47'
    >>> object_to_id(['a', 'b', 'c'])
    'eea457285a61f212e4bbaaf890263ab4'
    """
    return m9dicts.compat.md5(m9dicts.compat.to_str(obj)).hexdigest()


def _gen_id(*args):
    """
    :return: ID generated from `args`
    """
    return object_to_id(args)


def _rel_name(rel_name, key, level=0, names=None):
    """
    :return: Generated composite relation name from relations
    """
    if names is None:
        names = []
    name = "rel_%s_%s" % (rel_name, key)
    if name in names:
        name = "%s_%d" % (name, level)
    return name


def _sorted(items):
    """
    :param items: Any iterables
    """
    if items and m9dicts.utils.is_dict_like(items[0]):
        # return items  # Return as it is because dicts are not ordered.
        return sorted(items, key=lambda d: list(d.items()))
    else:
        return sorted(items)


def _dict_to_rels_itr_0(dic, key, rel_name, pid, **kwargs):
    """
    :param dic: A dict or dict-like object
    :param key: Key name
    :param rel_name: Name for parent relations
    :param pid: ID of parent object
    :param kwargs: Keyword arguments such as level, names
    """
    cid = dic.get("id", _gen_id(*sorted(dic.items())))
    name = _rel_name(rel_name, key, **kwargs)
    yield (name, ((key, cid), (rel_name, pid)))

    for tpl in _dict_to_rels_itr(dic, key, **kwargs):
        yield tpl


def _dict_to_rels_itr(dic, rel_name, level=0, names=None):
    """
    Convert nested dict[s] to tuples of relation name and relations of items in
    the dict, and yields each pairs.

    :param dic: A dict or dict-like object
    :param rel_name: Name for relations of items in `dic`
    :return: A list of (<relation_name>, [tuple of key and value])

    >>> list(_dict_to_rels_itr(dict(id=0, a=1, b="b"), "ab"))
    [('ab', (('id', 0), ('a', 1), ('b', 'b')))]

    >>> list(_dict_to_rels_itr(dict(id=0, a=dict(id=1, b=1), d="D"),
    ...                        "A"))  # doctest: +NORMALIZE_WHITESPACE
    [('A', (('id', 0), ('d', 'D'))),
     ('rel_A_a', (('a', 1), ('A', 0))),
     ('a', (('id', 1), ('b', 1)))]
    """
    if names is None:
        names = []
    else:
        names.append(rel_name)

    lkeys = [k for k, v in dic.items() if m9dicts.utils.is_list_like(v)]
    dkeys = [k for k, v in dic.items() if m9dicts.utils.is_dict_like(v)]
    items = sorted((k, v) for k, v in dic.items()
                   if k != "id" and k not in lkeys and k not in dkeys)
    pid = dic.get("id", _gen_id(*items))
    yield (rel_name, tuple([("id", pid)] + items))

    level += 1
    kwargs = dict(level=level, names=names)
    if lkeys:
        for key in sorted(lkeys):
            for val in _sorted(dic[key]):
                if m9dicts.utils.is_dict_like(val):
                    # :todo: Avoid name collision.
                    # if name in val:
                    #     ...
                    for tpl in _dict_to_rels_itr_0(val, key, rel_name, pid,
                                                   **kwargs):
                        yield tpl
                else:
                    cid = _gen_id(key, val)
                    yield (_rel_name(rel_name, key, **kwargs),
                           (("id", cid), (rel_name, pid), (key, val)))

    if dkeys:
        for key in sorted(dkeys):
            for tpl in _dict_to_rels_itr_0(dic[key], key, rel_name, pid,
                                           **kwargs):
                yield tpl


def dict_to_rels(dic, name=None):
    """
    Convert nested dict[s] to tuples of relation name and relations of items in
    the dict, and yields each pairs.

    :param dic: A dict or dict-like object
    :param name: Name for relations of items in `dic`
    :return: A list of (<relation_name>, [tuple of key and value])
    """
    assert m9dicts.utils.is_dict_like(dic)

    if name is None:
        name = "data"  # Default.

    fst = operator.itemgetter(0)
    rels = _dict_to_rels_itr(dic, name)
    return [(k, sorted(t[1] for t in g))
            for k, g in itertools.groupby(sorted(rels, key=fst), fst)]

# vim:sw=4:ts=4:et:
