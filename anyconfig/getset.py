#
# Copyright (C) 2014 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""Getter and setters of config objects loaded"""
import functools
import operator


def __parse_path_exp(path, seps=('/', '.')):
    """
    Parse path expression and return list of keys.

    :param path: Path expression may contain separator chars.
    :param seps: Separator char candidates.

    :return: A list of keys to fetch object[s] later.

    >>> __parse_path_exp('')
    []
    >>> __parse_path_exp('/a/b/c/d')
    ['a', 'b', 'c', 'd']
    >>> __parse_path_exp('a.b.c.d')
    ['a', 'b', 'c', 'd']
    >>> __parse_path_exp('abc')
    ['abc']
    """
    if not path:
        return []

    for sep in seps:
        if sep in path:
            return [x for x in path.split(sep) if x]

    return [path]


def __str_path(keys):
    """

    >>> __str_path(['a', 'b', 'c', 'd'])
    'a.b.c.d'
    """
    return '.'.join(keys)


def _get_recur(dic, path_keys=[], traversed=[]):
    """
    :param dic: Dict or dict-like object
    :param path_keys: List of path keys
    :param traversed: Traversed keys

    :return: (result, message) where result is a value or a dict/dict-like
        object pointed by `path_keys` or None means no result gotten or any
        error indicated by the message occured.

    >>> d = dict(a=dict(b=dict(c=0, d=1)))
    >>> _get_recur(d) == (d, '')
    True
    >>> _get_recur(d, ['a', 'b', 'c'])[0]
    0
    >>> _get_recur(d, ['a', 'b', 'd'])[0]
    1
    >>> _get_recur(d, ['a', 'b'])[0]
    {'c': 0, 'd': 1}
    >>> _get_recur(d, ['a', 'b', 'key_not_exist'])[0] is None
    True
    >>> _get_recur('a str', ['a'])[0] is None
    True
    """
    for key in path_keys:
        try:
            if key in dic:
                return _get_recur(dic[key], path_keys[1:], traversed + [key])
            else:
                path = __str_path(traversed + [key])
                return (None, "Not found at: " + path)

        except TypeError as e:
            path = __str_path(traversed + [key])
            return (None, "Not a dict at: {0}, err={1}".format(path, str(e)))

    return (dic, '')


def _get_reduce(dic, path_keys=[]):
    """
    Non recursive variant of _get_recur.

    :param dic: Dict or dict-like object
    :param path_keys: List of path keys

    >>> d = dict(a=dict(b=dict(c=0, d=1)))
    >>> _get_reduce(d)[0] == d
    True
    >>> _get_reduce(d, ['a', 'b', 'c'])[0]
    0
    >>> _get_reduce(d, ['a', 'b', 'd'])[0]
    1
    >>> _get_reduce(d, ['a', 'b'])[0]
    {'c': 0, 'd': 1}
    >>> _get_reduce(d, ['a', 'b', 'key_not_exist'])[0] is None
    True
    >>> _get_reduce('a str', ['a'])[0] is None
    True
    """
    try:
        return (functools.reduce(operator.getitem, path_keys, dic), '')
    except (TypeError, KeyError) as e:
        return (None, str(e))


def get(dic, path, sep='.', _get=_get_reduce):
    """
    :param dic: A dict or dict-like object to get result
    :param path: Path expression to point object wanted
    """
    (res, msg) = _get(dic, __parse_path_exp(path, (sep, )))
    return res

# vim:sw=4:ts=4:et:
