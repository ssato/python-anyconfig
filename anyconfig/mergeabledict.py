#
# Copyright (C) 2011 - 2015 Red Hat, Inc.
# Copyright (C) 2011 - 2013 Satoru SATOH <ssato redhat.com>
# License: MIT
#
"""Dict-based object supports merge operations.

.. versionchanged: 0.4.99
   Support to convert namedtuple objects from/to dicts recursively.

.. versionadded: 0.3.1
   Added naive and partial implementation of JSON Pointer support.

.. note:: JSON Pointer: http://tools.ietf.org/html/rfc6901
"""
from __future__ import absolute_import

import collections
import functools
import operator
import re

from .compat import iteritems, UserDict, OrderedDict
from anyconfig.utils import is_iterable


MS_REPLACE = "replace"
MS_NO_REPLACE = "noreplace"
MS_DICTS = "merge_dicts"
MS_DICTS_AND_LISTS = "merge_dicts_and_lists"

MERGE_STRATEGIES = (MS_REPLACE, MS_NO_REPLACE, MS_DICTS, MS_DICTS_AND_LISTS)

PATH_SEPS = ('/', '.')

_JSNP_GET_ARRAY_IDX_REG = re.compile(r"(?:0|[1-9][0-9]*)")
_JSNP_SET_ARRAY_IDX = re.compile(r"(?:0|[1-9][0-9]*|-)")

NAMEDTUPLE_CLS_KEY = "_namedtuple_cls_"


def jsnp_unescape(jsn_s):
    """
    Parse and decode given encoded JSON Pointer expression, convert ~1 to
    / and ~0 to ~.

    >>> jsnp_unescape("/a~1b")
    '/a/b'
    >>> jsnp_unescape("~1aaa~1~0bbb")
    '/aaa/~bbb'
    """
    return jsn_s.replace('~1', '/').replace('~0', '~')


def parse_path(path, seps=PATH_SEPS):
    """
    Parse path expression and return list of path items.

    :param path: Path expression may contain separator chars.
    :param seps: Separator char candidates.

    :return: A list of keys to fetch object[s] later.

    >>> parse_path('')
    []
    >>> parse_path('/')  # JSON Pointer spec expects this behavior.
    ['']
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
            if path == sep:  # Special case, '/' or '.' only.
                return ['']
            return [x for x in path.split(sep) if x]

    return [path]


def get(dic, path, seps=PATH_SEPS):
    """
    getter for nested dicts.

    .. versionchanged: 0.3.1
       Added naive and partial implementation of JSON Pointer support

    :param dic: Dict or dict-like object
    :param path: Path expression to point object wanted
    :param seps: Separator char candidates

    :return: A tuple of (result_object, error_message)

    >>> d = {'a': {'b': {'c': 0, 'd': [1, 2]}}, '': 3}
    >>> get(d, '/')  # key becomes '' (empty string).
    (3, '')
    >>> get(d, "/a/b/c")
    (0, '')
    >>> sorted(get(d, "a.b")[0].items())
    [('c', 0), ('d', [1, 2])]
    >>> (get(d, "a.b.d"), get(d, "/a/b/d/1"))
    (([1, 2], ''), (2, ''))
    >>> get(d, "a.b.key_not_exist")  # doctest: +ELLIPSIS
    (None, "'...'")
    >>> get(d, "/a/b/d/2")
    (None, 'list index out of range')
    >>> get(d, "/a/b/d/-")  # doctest: +ELLIPSIS
    (None, 'list indices must be integers...')
    """
    items = [jsnp_unescape(p) for p in parse_path(path, seps)]
    if not items:
        return (dic, '')
    try:
        if len(items) == 1:
            return (dic[items[0]], '')

        parent = functools.reduce(operator.getitem, items[:-1], dic)

        if is_iterable(parent) and _JSNP_GET_ARRAY_IDX_REG.match(items[-1]):
            return (parent[int(items[-1])], '')
        else:
            return (parent[items[-1]], '')

    except (TypeError, KeyError, IndexError) as exc:
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
    for key in reversed(parse_path(path, seps)):
        ret = {key: val if ret is None else ret.copy()}

    return ret


def set_(dic, path, val, seps=PATH_SEPS, strategy=None):
    """
    setter for nested dicts.

    :param dic: MergeableDict instance or other dict-like objects support
        recursive merge operations.
    :param path: Path expression to point object wanted
    :param seps: Separator char candidates.

    >>> d = create_from(dict(a=1, b=dict(c=2, )))
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
    return isinstance(obj, (dict, collections.Mapping, UserDict))


def is_namedtuple(obj):
    """
    >>> p0 = collections.namedtuple("Point", "x y")(1, 2)
    >>> is_namedtuple(p0)
    True
    >>> is_namedtuple(tuple(p0))
    False
    """
    return isinstance(obj, tuple) and hasattr(obj, "_asdict")


def convert_to(obj, to_namedtuple=False,
               _namedtuple_cls_key=NAMEDTUPLE_CLS_KEY):
    """
    Convert a OrderedMergeableDict or MergeableDict instances to a dict or
    namedtuple object recursively.

    Borrowed basic idea and implementation from bunch.unbunchify.
    (bunch is distributed under MIT license same as this module.)

    .. note::
       If `to_namedtuple` is True and given object `obj` is MergeableDict and
       not OrderedMergeableDict, then the order of fields of result namedtuple
       object may be random and not stable because the order of MergeableDict
       may not be kept and stable.

    .. note::
       namedtuple object cannot have fields start with '_' because it may be
       conflicts with special methods of object like '__class__'. So it'll fail
       if to convert dicts has such keys.

    :param obj: An [Ordered]MergeableDict instance or other object
    :param to_namedtuple:
        Convert `obj` to namedtuple object of which definition is created on
        the fly if True instead of dict.
    :param _namedtuple_cls_key:
        Special keyword to embedded the class name of namedtuple object to
        create.  See the comments in :func:`create_from` also.

    :return: A dict or namedtuple object if to_namedtuple is True
    """
    if is_dict_like(obj):
        if to_namedtuple:
            _name = obj.get(_namedtuple_cls_key, "NamedTuple")
            _keys = [k for k in obj.keys() if k != _namedtuple_cls_key]
            _vals = [convert_to(obj[k], to_namedtuple, _namedtuple_cls_key)
                     for k in _keys]
            return collections.namedtuple(_name, _keys)(*_vals)
        else:
            return dict((k, convert_to(v)) for k, v in iteritems(obj))
    elif is_namedtuple(obj):
        if to_namedtuple:
            return obj  # Nothing to do if it's nested n.t. (it should be).
        else:
            return dict((k, convert_to(getattr(obj, k))) for k in obj._fields)
    elif is_iterable(obj):
        return type(obj)(convert_to(v, to_namedtuple, _namedtuple_cls_key)
                         for v in obj)
    else:
        return obj


def create_from(obj=None, ac_ordered=False,
                _namedtuple_cls_key=NAMEDTUPLE_CLS_KEY):
    """
    Try creating a MergeableDict instance[s] from a dict or any other objects.

    :param obj: A dict instance or None
    :param ac_ordered:
        Create an instance of OrderedMergeableDict instead of MergeableDict If
        it's True. Please note that OrderedMergeableDict class will be chosen
        for namedtuple objects regardless of this argument always to keep keys
        (fields) order.
    :param _namedtuple_cls_key:
        Special keyword to embedded the class name of namedtuple object to the
        MergeableDict object created. It's a hack and not elegant but I don't
        think there are another ways to make same namedtuple object from the
        MergeableDict object created from it.
    """
    cls = OrderedMergeableDict if ac_ordered else MergeableDict
    if obj is None:
        return cls()

    opts = dict(ac_ordered=ac_ordered, _namedtuple_cls_key=_namedtuple_cls_key)
    if is_dict_like(obj):
        return cls((k, create_from(v, **opts)) for k, v in iteritems(obj))
    elif is_namedtuple(obj):
        mdict = OrderedMergeableDict((k, create_from(getattr(obj, k), **opts))
                                     for k in obj._fields)
        mdict[_namedtuple_cls_key] = obj.__class__.__name__
        return mdict
    elif is_iterable(obj):
        return type(obj)(create_from(v, **opts) for v in obj)
    else:
        return obj


class MergeableDict(dict):
    """Dict based object supports 'merge' operation.
    """
    strategy = MS_DICTS

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

        >>> md0 = create_from(dict(a=1, b=[1, 3], c="abc"))
        >>> md1 = create_from(dict(a=2, b=[0, 1], c="xyz"))
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

        >>> md0 = md1 = create_from(dict(a=1, b=[1, 3], c="abc"))
        >>> md2 = create_from(dict(a=2, b=[0, 1], c="xyz", d=None))
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

        >>> md0 = md1 = create_from(dict(a=1, b=dict(c=2, d=3),
        ...                                       e=[1, 2, 2]))
        >>> md2 = create_from(dict(a=2, b=dict(d=4, f=5),
        ...                                 e=[2, 3, 4]))
        >>> md0.update_w_merge(md2, False)
        >>> md0["a"] == md2["a"]
        True
        >>> md0["b"]["d"] == md2["b"]["d"] and md0["b"]["f"] == md2["b"]["f"]
        True
        >>> md0["e"] == md2["e"]
        True

        >>> md3 = create_from(dict(aaa=[1, 2, 3], ))
        >>> md4 = create_from(dict(aaa=[4, 4, 5], ))
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


class OrderedMergeableDict(OrderedDict, MergeableDict):
    """MergeableDict keeps order of keys.
    """
    pass

# vim:sw=4:ts=4:et:
