#
# Copyright (C) 2011 - 2016 Satoru SATOH <ssato at redhat.com>
#
# pylint: disable=missing-docstring
from __future__ import absolute_import


def dicts_equal(lhs, rhs):
    """
    >>> dicts_equal({}, {})
    True
    >>> dicts_equal({}, {'a': 1})
    False
    >>> d0 = {'a': 1}; dicts_equal(d0, d0)
    True
    >>> d1 = {'a': [1, 2, 3]}; dicts_equal(d1, d1)
    True
    >>> dicts_equal(d0, d1)
    False
    """
    if len(lhs.keys()) != len(rhs.keys()):
        return False

    for key, val in rhs.items():
        val_ref = lhs.get(key, None)
        if val != val_ref:
            return False

    return True

# vim:sw=4:ts=4:et:
