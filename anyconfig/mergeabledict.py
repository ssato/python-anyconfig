#
# Copyright (C) 2011 - 2015 Red Hat, Inc.
# Copyright (C) 2011 - 2013 Satoru SATOH <ssato redhat.com>
# License: MIT
#
"""Merge-able dict.
"""
from __future__ import absolute_import
from .compat import iteritems

import collections
import functools
import operator

import anyconfig.parser
import anyconfig.utils

from anyconfig.utils import is_iterable

# TODO: Keep items' order:
# from collections import OrderedDict as dict


MS_REPLACE = "replace"
MS_NO_REPLACE = "noreplace"
MS_DICTS = "merge_dicts"
MS_DICTS_AND_LISTS = "merge_dicts_and_lists"

MERGE_STRATEGIES = (MS_REPLACE, MS_NO_REPLACE, MS_DICTS, MS_DICTS_AND_LISTS)

PATH_SEPS = ('/', '.')


def parse_path(path, seps=PATH_SEPS):
    """
    Parse path expression and return list of path items.

    :param path: Path expression may contain separator chars.
    :param seps: Separator char candidates.

    :return: A list of keys to fetch object[s] later.

    >>> parse_path('')
    []
    >>> parse_path('/a') == parse_path('.a') == ['a']
    True
    >>> parse_path('a') == parse_path('a.') == ['a']
    True
    >>> parse_path('/a/b/c') == parse_path('a.b.c') == ['a', 'b', 'c']
    True
    >>> parse_path('abc')
    ['abc']
    """
    if not path:
        return []

    for sep in seps:
        if sep in path:
            return [x for x in path.split(sep) if x]

    return [path]


def get(dic, path, seps=PATH_SEPS):
    """
    getter for nested dicts.

    :param dic: Dict or dict-like object
    :param path: Path expression to point object wanted
    :param seps: Separator char candidates.

    >>> d = dict(a=dict(b=dict(c=0, d=1)))
    >>> get(d, '/') == (d, '')
    True
    >>> get(d, "/a/b/c")
    (0, '')
    >>> get(d, "a.b.d")
    (1, '')
    >>> get(d, "a.b") == ({'c': 0, 'd': 1}, '')
    True
    >>> get(d, "a.b.key_not_exist")[0] is None
    True
    >>> get('a str', 'a')[0] is None
    True
    """
    try:
        return (functools.reduce(operator.getitem,
                                 anyconfig.parser.parse_path(path, seps),
                                 dic),
                '')
    except (TypeError, KeyError) as exc:
        return (None, str(exc))


def mk_nested_dic(path, val, seps=PATH_SEPS):
    """
    Make a nested dict iteratively.

    :param path: Path expression to make a nested dict
    :param val: Value to set
    :param seps: Separator char candidates

    >>> mk_nested_dic("a.b.c", 1)
    {'a': {'b': {'c': 1}}}
    >>> mk_nested_dic("/a/b/c", 1)
    {'a': {'b': {'c': 1}}}
    """
    ret = None
    for key in reversed(anyconfig.parser.parse_path(path, seps)):
        ret = {key: val if ret is None else ret.copy()}

    return ret


def set_(dic, path, val, seps=PATH_SEPS, strategy=None):
    """
    setter for nested dicts.

    :param dic: MergeableDict instance or other dict-like objects support
        recursive merge operations.
    :param path: Path expression to point object wanted
    :param seps: Separator char candidates.

    >>> d = MergeableDict.create(dict(a=1, b=dict(c=2, )))
    >>> set_(d, 'a.b.d', 3)
    >>> d['a']['b']['d']
    3
    """
    diff = mk_nested_dic(path, val, seps)
    dic.update(diff, strategy)


def is_dict_like(obj):
    """
    :param obj: Any object may be an instance of MergeableDict or dict.

    >>> is_dict_like("a string")
    False
    >>> is_dict_like({})
    True
    >>> is_dict_like(create_from({}))
    True
    """
    return isinstance(obj, (dict, collections.Mapping))


def convert_to(mdict):
    """
    Convert a MergeableDict instances to a dict object.

    Borrowed basic idea and implementation from bunch.unbunchify.
    (bunch is distributed under MIT license same as this module.)

    :param mdict: A MergeableDict instance
    :return: A dict
    """
    if is_dict_like(mdict):
        return dict((k, convert_to(v)) for k, v in iteritems(mdict))
    elif is_iterable(mdict):
        return type(mdict)(convert_to(v) for v in mdict)
    else:
        return mdict


def create_from(dic):
    """
    Try creating a MergeableDict instance[s] from a dict or any other objects.

    :param dic: A dict instance
    """
    if is_dict_like(dic):
        return MergeableDict((k, create_from(v)) for k, v in iteritems(dic))
    elif is_iterable(dic):
        return type(dic)(create_from(v) for v in dic)
    else:
        return dic


class MergeableDict(dict):
    """
    Dict based object supports 'merge' operation.
    """

    strategy = MS_DICTS

    @classmethod
    def create(cls, obj):
        """Create an instance from any object."""
        return create_from(obj)

    @classmethod
    def convert_to(cls, mdict):
        """Create an object from MergeableDict instances"""
        return convert_to(mdict)

    def get_strategy(self):
        """Merge strategy"""
        return self.strategy

    def update(self, other, strategy=None, keep=False):
        """Update members recursively based on given strategy.

        :param other: Other MergeableDict instance to merge
        :param strategy: Merge strategy
        :param keep:
            Keep original value if type of original value is not a dict nor
            list.  It will be simply replaced with new value by default.
        """
        if strategy is None:
            strategy = self.get_strategy()

        if strategy == MS_REPLACE:
            self.update_w_replace(other)
        elif strategy == MS_NO_REPLACE:
            self.update_wo_replace(other)
        elif strategy == MS_DICTS_AND_LISTS:
            self.update_w_merge(other, merge_lists=True, keep=keep)
        else:
            self.update_w_merge(other, merge_lists=False, keep=keep)

    def update_w_replace(self, other):
        """Update and replace self w/ other if both has same keys.

        :param other: object of which type is same as self's.

        >>> md0 = MergeableDict.create(dict(a=1, b=[1, 3], c="abc"))
        >>> md1 = MergeableDict.create(dict(a=2, b=[0, 1], c="xyz"))
        >>> md0.update_w_replace(md1)
        >>> all(md0[k] == md1[k] for k in ("a", "b", "c"))
        True
        """
        if is_dict_like(other):
            for key, val in iteritems(other):
                self[key] = val

    def update_wo_replace(self, other):
        """Update self w/ other but never replace self w/ other.

        :param other: object of which type is same as self's.

        >>> md0 = md1 = MergeableDict.create(dict(a=1, b=[1, 3], c="abc"))
        >>> md2 = MergeableDict.create(dict(a=2, b=[0, 1], c="xyz", d=None))
        >>> md0.update_wo_replace(md2)
        >>> all(md0[k] != md2[k] for k in ("a", "b", "c"))
        True
        >>> all(md0[k] == md1[k] for k in ("a", "b", "c"))
        True
        >>> md0["d"] == md2["d"]
        True
        """
        if is_dict_like(other):
            for key, val in iteritems(other):
                if key not in self:
                    self[key] = val

    def update_w_merge(self, other, merge_lists=False, keep=False):
        """
        Merge members recursively. Behavior of merge will be vary depends on
        types of original and new values.

        - dict vs. dict -> merge recursively
        - list vs. list -> vary depends on `merge_lists`. see its description.
        - other objects vs. any -> vary depends on `keep`. see its description.

        :param merge_lists: Merge not only dicts but also lists. For example,

            [1, 2, 3], [3, 4] ==> [1, 2, 3, 4]
            [1, 2, 2], [2, 4] ==> [1, 2, 2, 4]

        :param keep:
            Keep original value if type of original value is not a dict nor
            list.  It will be simply replaced with new value by default.

        >>> md0 = md1 = MergeableDict.create(dict(a=1, b=dict(c=2, d=3),
        ...                                       e=[1, 2, 2]))
        >>> md2 = MergeableDict.create(dict(a=2, b=dict(d=4, f=5),
        ...                                 e=[2, 3, 4]))
        >>> md0.update_w_merge(md2, False)
        >>> md0["a"] == md2["a"]
        True
        >>> md0["b"]["d"] == md2["b"]["d"] and md0["b"]["f"] == md2["b"]["f"]
        True
        >>> md0["e"] == md2["e"]
        True

        >>> md3 = MergeableDict.create(dict(aaa=[1, 2, 3], ))
        >>> md4 = MergeableDict.create(dict(aaa=[4, 4, 5], ))
        >>> md3.update_w_merge(md4, True)
        >>> md3["aaa"] == [1, 2, 3, 4, 4, 5]
        True
        """
        if not is_dict_like(other):
            return

        for key, val in iteritems(other):
            val0 = self.get(key, None)  # Original value

            if val0 is None:
                self[key] = val
                continue

            if is_dict_like(val0):  # It needs recursive updates.
                self[key].update_w_merge(val, merge_lists, keep)
            elif merge_lists and is_iterable(val) and is_iterable(val0):
                self[key] += [x for x in list(val) if x not in val0]
            elif not keep:
                self[key] = val  # Overwrite it.

# vim:sw=4:ts=4:et:
