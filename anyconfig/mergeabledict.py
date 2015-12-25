#
# Copyright (C) 2011 - 2015 Red Hat, Inc.
# Copyright (C) 2011 - 2013 Satoru SATOH <ssato redhat.com>
# License: MIT
#
"""Dict-based object supports merge operations.

.. versionchanged: 0.4.99

   - support to convert namedtuple objects from/to mergeable dicts recursively.
   - split MergeableDict into some classes to make these update methods worked
     like dict.update, and remove MergeableDict class to eliminate bogus
     update_* methods.
   - make create_from() works as factory function of various mergeable dict
     classes.

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


class UpdateWithReplaceDict(dict):
    """
    Replace self with other if both has same keys on update.

    >>> od0 = OrderedDict((("a", 1), ("b", [1, 3]), ("c", "abc"), ("f", None)))
    >>> md0 = UpdateWithReplaceDict(od0)
    >>> md1 = UpdateWithReplaceDict(od0.items())
    >>> ref = md0.copy()
    >>> upd = UpdateWithReplaceDict(a=2, b=[0, 1], c=dict(d="d", e=1), d="d")
    >>> md0.update(upd)
    >>> md1.update(upd)
    >>> all(md0[k] == upd[k] for k in upd.keys())
    True
    >>> all(md0[k] == ref[k] for k in ref.keys() if k not in upd)
    True
    >>> all(md1[k] == upd[k] for k in upd.keys())
    True
    >>> all(md1[k] == ref[k] for k in ref.keys() if k not in upd)
    True
    >>> md2 = UpdateWithReplaceDict(1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    def _update(self, other, key, *args):
        """
        :param other:
            dict or dict-like object or a list of (key, value) pair tuples
        :param key: object key
        :param args: [] or (value, ...)
        """
        self[key] = args[0] if args else other[key]

    def update(self, *others, **another):
        """
        :param others:
            a list of dict or dict-like objects or a list of (key, value) pair
            tuples to update self
        :param another: optional keyword arguments to update self more

        .. seealso:: Document of dict.update
        """
        for other in others:
            if hasattr(other, "keys"):
                for key in other.keys():
                    self._update(other, key)
            else:
                for key, val in other:  # TypeError, etc. may be raised.
                    self._update(other, key, val)

        for key in another.keys():
            self._update(another, key)


class UpdateWoReplaceDict(UpdateWithReplaceDict):
    """
    Update self w/ other but never replace self w/ other if both objects have
    same keys.

    >>> od0 = OrderedDict((("a", 1), ("b", [1, 3]), ("c", "abc"),
    ...                    ("f", None)))
    >>> md0 = UpdateWoReplaceDict(od0)
    >>> ref = md0.copy()
    >>> upd = UpdateWoReplaceDict(a=2, b=[0, 1], c="xyz", d=None)
    >>> md0.update(upd)
    >>> all(md0[k] == upd[k] for k in upd.keys() if k not in ref)
    True
    >>> all(md0[k] == ref[k] for k in ref.keys())
    True
    """
    def _update(self, other, key, *args):
        """
        :param other:
            dict or dict-like object or a list of (key, value) pair tuples
        :param key: object key
        :param args: [] or (value, ...)
        """
        if key not in self:
            self[key] = args[0] if args else other[key]


class UpdateWithMergeDict(UpdateWithReplaceDict):
    """
    Merge members recursively. Behavior of merge will be vary depends on
    types of original and new values.

    - dict vs. dict -> merge recursively
    - list vs. list -> vary depends on `merge_lists`. see its description.
    - other objects vs. any -> vary depends on `keep`. see its description.

    class variables:

        - merge_lists: Merge not only dicts but also lists. For example,

            [1, 2, 3], [3, 4] ==> [1, 2, 3, 4]
            [1, 2, 2], [2, 4] ==> [1, 2, 2, 4]

        - keep: Keep original value if type of original value is not a dict nor
          list. It will be simply replaced with new value by default.

    >>> od0 = OrderedDict((("c", 2), ("d", 3)))
    >>> od1 = OrderedDict((("c", 4), ("d", 5), ("g", None)))
    >>> md0 = UpdateWithMergeDict((("a", 1),
    ...                            ("b", UpdateWithMergeDict(od0)),
    ...                            ("e", [1, 2, 2]), ("f", None)))
    >>> ref = md0.copy()
    >>> upd = UpdateWithMergeDict((("a", 2),
    ...                            ("b", UpdateWithMergeDict(od1)),
    ...                            ("e", [2, 3, 4])))
    >>> md0.update(upd)
    >>> all(md0[k] == upd[k] for k in ("a", "e"))  # vary depends on 'keep'.
    True
    >>> all(md0["b"][k] == ref["b"][k] for k in ref["b"].keys())
    True
    >>> all(md0[k] == ref[k] for k in ref.keys() if k not in upd)
    True
    """
    merge_lists = False
    keep = False

    def _update(self, other, key, *args):
        """
        :param other:
            dict or dict-like object or a list of (key, value) pair tuples
        :param key: object key
        :param args: [] or (value, ...)
        """
        val = args[0] if args else other[key]
        if key in self:
            val0 = self[key]  # Original value
            if is_dict_like(val0):  # It needs recursive updates.
                self[key].update(val)
            elif self.merge_lists and is_iterable(val) and is_iterable(val0):
                self[key] += [x for x in val if x not in val0]
            elif not self.keep:
                self[key] = val  # Overwrite it.
        else:
            self[key] = val


class UpdateWithMergeListsDict(UpdateWithMergeDict):
    """
    Similar to UpdateWithMergeDict but merge lists by default.

    >>> md0 = UpdateWithMergeListsDict(aaa=[1, 2, 3])
    >>> upd = UpdateWithMergeListsDict(aaa=[4, 4, 5])
    >>> md0.update(upd)
    >>> md0["aaa"]
    [1, 2, 3, 4, 4, 5]
    """
    merge_lists = True


class UpdateWithReplaceOrderedDict(UpdateWithReplaceDict, OrderedDict):
    """
    Similar to UpdateWithReplaceDict but keep keys' order like OrderedDict.

    >>> od0 = OrderedDict((("a", 1), ("b", [1, 3]), ("c", "abc"), ("f", None)))
    >>> od1 = OrderedDict((("a", 2), ("b", [0, 1]),
    ...                    ("c", OrderedDict((("d", "d"), ("e", 1)))),
    ...                    ("d", "d")))
    >>> md0 = UpdateWithReplaceOrderedDict(od0)
    >>> md1 = UpdateWithReplaceOrderedDict(od0.items())
    >>> ref = md0.copy()
    >>> upd = UpdateWithReplaceOrderedDict(od1)
    >>> md0.update(upd)
    >>> md1.update(upd)
    >>> all(md0[k] == upd[k] for k in upd.keys())
    True
    >>> all(md0[k] == ref[k] for k in ref.keys() if k not in upd)
    True
    >>> all(md1[k] == upd[k] for k in upd.keys())
    True
    >>> all(md1[k] == ref[k] for k in ref.keys() if k not in upd)
    True
    >>> list(md0.keys())
    ['a', 'b', 'c', 'f', 'd']
    >>> list(md1.keys())
    ['a', 'b', 'c', 'f', 'd']
    """
    pass


class UpdateWoReplaceOrderedDict(UpdateWoReplaceDict, OrderedDict):
    """
    Similar to UpdateWoReplaceDict but keep keys' order like OrderedDict.

    >>> od0 = OrderedDict((("a", 1), ("b", [1, 3]), ("c", "abc"),
    ...                    ("f", None)))
    >>> md0 = UpdateWoReplaceOrderedDict(od0)
    >>> ref = md0.copy()
    >>> md1 = UpdateWoReplaceOrderedDict((("a", 2), ("b", [0, 1]),
    ...                                   ("c", "xyz"), ("d", None)))
    >>> md0.update(md1)
    >>> all(md0[k] == md1[k] for k in md1.keys() if k not in ref)
    True
    >>> all(md0[k] == ref[k] for k in ref.keys())
    True
    >>> list(md0.keys())
    ['a', 'b', 'c', 'f', 'd']
    """
    pass


class UpdateWithMergeOrderedDict(UpdateWithMergeDict, OrderedDict):
    """
    Similar to UpdateWithMergeDict but keep keys' order like OrderedDict.

    >>> od0 = OrderedDict((("c", 2), ("d", 3)))
    >>> od1 = OrderedDict((("c", 4), ("d", 5), ("g", None)))
    >>> md0 = UpdateWithMergeOrderedDict(
    ...          OrderedDict((("a", 1),
    ...                       ("b", UpdateWithMergeOrderedDict(od0)),
    ...                       ("e", [1, 2, 2]), ("f", None))))
    >>> ref = md0.copy()
    >>> upd = dict(a=2, b=UpdateWithMergeOrderedDict(od1), e=[2, 3, 4])
    >>> md0.update(upd)
    >>> all(md0[k] == upd[k] for k in ("a", "e"))  # vary depends on 'keep'.
    True
    >>> all(md0[k] == ref[k] for k in ref.keys() if k not in upd)
    True
    >>> all(md0["b"][k] == ref["b"][k] for k in ref["b"].keys())
    True
    >>> list(md0.keys())
    ['a', 'b', 'e', 'f']
    >>> list(md0["b"].keys())
    ['c', 'd', 'g']
    """
    pass


class UpdateWithMergeListsOrderedDict(UpdateWithMergeListsDict, OrderedDict):
    """
    Similar to UpdateWithMergeListsDict but keep keys' order like OrderedDict.

    >>> md0 = UpdateWithMergeListsOrderedDict((("aaa", [1, 2, 3]), ('b', 0)))
    >>> upd = UpdateWithMergeListsOrderedDict((("aaa", [4, 4, 5]), ))
    >>> md0.update(upd)
    >>> md0["aaa"]
    [1, 2, 3, 4, 4, 5]
    >>> list(md0.keys())
    ['aaa', 'b']
    """
    pass


# Alias to keep backward compatibility for a while.
MergeableDict = UpdateWithMergeDict


def convert_to(obj, to_namedtuple=False, _ac_ntpl_cls_key=NAMEDTUPLE_CLS_KEY,
               **opts):
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
    :param _ac_ntpl_cls_key:
        Special keyword to embedded the class name of namedtuple object to
        create.  See the comments in :func:`create_from` also.
    :param opts: Extra optional keyword arguments such as ac_ordered:

        - ac_ordered: Create an OrderedDict object instead of dict if True

    :return: A dict or namedtuple object if to_namedtuple is True
    """
    cls = OrderedDict if opts.get("ac_ordered", False) else dict
    if is_dict_like(obj):
        if to_namedtuple:
            _name = obj.get(_ac_ntpl_cls_key, "NamedTuple")
            _keys = [k for k in obj.keys() if k != _ac_ntpl_cls_key]
            _vals = [convert_to(obj[k], to_namedtuple, _ac_ntpl_cls_key,
                                **opts) for k in _keys]
            return collections.namedtuple(_name, _keys)(*_vals)
        else:
            return cls((k, convert_to(v, **opts)) for k, v in iteritems(obj))
    elif is_namedtuple(obj):
        if to_namedtuple:
            return obj  # Nothing to do if it's nested n.t. (it should be).
        else:
            return cls((k, convert_to(getattr(obj, k))) for k in obj._fields)
    elif is_iterable(obj):
        return type(obj)(convert_to(v, to_namedtuple, _ac_ntpl_cls_key, **opts)
                         for v in obj)
    else:
        return obj


# Mapppings: (merge_strategy, ordered?) : mergeable dict class
_MS_CLASS_MAP = {(MS_REPLACE, True): UpdateWithReplaceOrderedDict,
                 (MS_REPLACE, False): UpdateWithReplaceDict,
                 (MS_NO_REPLACE, True): UpdateWoReplaceOrderedDict,
                 (MS_NO_REPLACE, False): UpdateWoReplaceDict,
                 (MS_DICTS, True): UpdateWithMergeOrderedDict,
                 (MS_DICTS, False): UpdateWithMergeDict,
                 (MS_DICTS_AND_LISTS, True): UpdateWithMergeListsOrderedDict,
                 (MS_DICTS_AND_LISTS, False): UpdateWithMergeListsDict}

# Hack: mappings from non-ordered version of mdict to ordered one.
_MDICTS_CLASS_MAP = {UpdateWithReplaceDict: UpdateWithReplaceOrderedDict,
                     UpdateWoReplaceDict: UpdateWoReplaceOrderedDict,
                     UpdateWithMergeDict: UpdateWithMergeOrderedDict,
                     UpdateWithMergeListsDict: UpdateWithMergeListsOrderedDict}


def _get_mdict_class(ac_merge=MS_DICTS, ac_ordered=False):
    """
    :param ac_merge:
        Specify strategy from MERGE_STRATEGIES of how to merge results loaded
        from multiple configuration files.
    :param ac_ordered:
        Create an instance of OrderedMergeableDict instead of MergeableDict If
        it's True. Please note that OrderedMergeableDict class will be chosen
        for namedtuple objects regardless of this argument always to keep keys
        (fields) order.
    """
    return _MS_CLASS_MAP.get((ac_merge, ac_ordered), UpdateWithMergeDict)


def create_from(obj=None, ac_ordered=False,
                _ac_ntpl_cls_key=NAMEDTUPLE_CLS_KEY, **options):
    """
    Try creating a MergeableDict instance[s] from a dict or any other objects.

    :param obj: A dict instance or None
    :param ac_ordered:
        Create an instance of OrderedMergeableDict instead of MergeableDict If
        it's True. Please note that OrderedMergeableDict class will be chosen
        for namedtuple objects regardless of this argument always to keep keys
        (fields) order.
    :param _ac_ntpl_cls_key:
        Special keyword to embedded the class name of namedtuple object to the
        MergeableDict object created. It's a hack and not elegant but I don't
        think there are another ways to make same namedtuple object from the
        MergeableDict object created from it.
    :param options: Other keyword arguments such as:

        - ac_merge: Specify strategy from MERGE_STRATEGIES of how to merge
          results loaded from multiple configuration files.
    """
    ac_merge = options.get("ac_merge", MS_DICTS)
    if ac_merge not in MERGE_STRATEGIES:
        raise ValueError("Wrong merge strategy: %r" % ac_merge)

    if getattr(options, "ac_namedtuple", False):
        ac_ordered = True  # To keep the order of items.

    cls = _get_mdict_class(ac_merge=ac_merge, ac_ordered=ac_ordered)
    if obj is None:
        return cls()

    opts = dict(ac_ordered=ac_ordered, _ac_ntpl_cls_key=_ac_ntpl_cls_key)
    opts.update(options)

    if is_dict_like(obj):
        return cls((k, None if v is None else create_from(v, **opts)) for k, v
                   in iteritems(obj))
    elif is_namedtuple(obj):
        ocls = _MDICTS_CLASS_MAP[cls]
        mdict = ocls((k, create_from(getattr(obj, k), **opts)) for k
                     in obj._fields)
        mdict[_ac_ntpl_cls_key] = obj.__class__.__name__
        return mdict
    elif is_iterable(obj):
        return type(obj)(create_from(v, **opts) for v in obj)
    else:
        return obj


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
    if strategy is None:
        strategy = MS_DICTS
    cls = _get_mdict_class(ac_merge=strategy)
    diff = cls(mk_nested_dic(path, val, seps))
    dic.update(diff)

# vim:sw=4:ts=4:et:
