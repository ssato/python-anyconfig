#
# Copyright (C) 2014 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""Getter and setters of config objects loaded"""
from .globals import LOGGER as logging
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


def __get(dic, path_keys=[], traversed_keys=[]):
    """
    :param dic: Dict or dict-like object
    :param path_keys: List of path keys
    :param traversed_keys: Traversed keys

    :return: (result, message) where result is a value or a dict/dict-like
        object pointed by `path_keys` or None means no result gotten or any
        error indicated by the message occured.

    >>> d = dict(a=dict(b=dict(c=0, d=1)))
    >>> __get(d) == (d, '')
    True
    >>> __get(d, ['a', 'b', 'c'])[0]
    0
    >>> __get(d, ['a', 'b', 'd'])[0]
    1
    >>> __get(d, ['a', 'b'])[0]
    {'c': 0, 'd': 1}
    >>> __get(d, ['a', 'b', 'key_not_exist'])[0] is None
    True
    >>> __get('a str', ['a'])[0] is None
    True
    """
    for key in path_keys:
        try:
            if key in dic:
                return __get(dic[key], path_keys[1:], traversed_keys + [key])
            else:
                path = __str_path(traversed_keys + [key])
                return (None, "Not found at: " + path)

        except TypeError as e:
            logging.error(str(e))
            path = __str_path(traversed_keys + [key])
            return (None, "Not a dict at: " + path)

    return (dic, '')


def __get_2(dic, path_keys=[], traversed_keys=[]):
    """
    Non recursive variant of __get.

    :param dic: Dict or dict-like object
    :param path_keys: List of path keys

    >>> d = dict(a=dict(b=dict(c=0, d=1)))
    >>> __get_2(d) == d
    True
    >>> __get_2(d, ['a', 'b', 'c'])
    0
    >>> __get_2(d, ['a', 'b', 'd'])
    1
    >>> __get_2(d, ['a', 'b'])
    {'c': 0, 'd': 1}
    >>> __get_2(d, ['a', 'b', 'key_not_exist']) is None
    True
    >>> __get_2('a str', ['a']) is None
    True
    """
    try:
        return functools.reduce(operator.getitem, path_keys, dic)
    except (TypeError, KeyError) as e:
        logging.error(str(e))
        return None


def get(dic, path, sep='.'):
    """
    :param dic: A dict or dict-like object to get result
    :param path: Path expression to point object wanted
    """
    (res, msg) = __get(dic, __parse_path_exp(path, (sep, )))
    return res

# vim:sw=4:ts=4:et:
