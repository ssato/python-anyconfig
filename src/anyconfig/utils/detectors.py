#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Functions to detect something.
"""
import collections.abc
import types
import typing


GLOB_MARKER = '*'


def is_iterable(obj: typing.Any) -> bool:
    """
    >>> is_iterable([])
    True
    >>> is_iterable(())
    True
    >>> is_iterable([x for x in range(10)])
    True
    >>> is_iterable((1, 2, 3))
    True
    >>> g = (x for x in range(10))
    >>> is_iterable(g)
    True
    >>> is_iterable('abc')
    False
    >>> is_iterable(0)
    False
    >>> is_iterable({})
    False
    """
    return isinstance(obj, (list, tuple, types.GeneratorType)) or \
        (not isinstance(obj, (int, str, dict)) and
         bool(getattr(obj, 'next', False)))


def is_dict_like(obj: typing.Any) -> bool:
    """
    :param obj: Any object behaves like a dict.

    >>> is_dict_like('a string')
    False
    >>> is_dict_like({})
    True
    >>> import collections
    >>> is_dict_like(collections.OrderedDict((('a', 1), ('b', 2))))
    True
    """
    return isinstance(obj, (dict, collections.abc.Mapping))  # any others?


_LIST_LIKE_TYPES = (collections.abc.Iterable, collections.abc.Sequence)


def is_list_like(obj: typing.Any) -> bool:
    """
    >>> is_list_like([])
    True
    >>> is_list_like(())
    True
    >>> is_list_like([x for x in range(10)])
    True
    >>> is_list_like((1, 2, 3))
    True
    >>> g = (x for x in range(10))
    >>> is_list_like(g)
    True
    >>> is_list_like('abc')
    False
    >>> is_list_like(0)
    False
    >>> is_list_like({})
    False
    """
    return isinstance(obj, _LIST_LIKE_TYPES) and \
        not (isinstance(obj, str) or is_dict_like(obj))

# vim:sw=4:ts=4:et:
