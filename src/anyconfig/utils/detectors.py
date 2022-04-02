#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Functions to detect something."""
import collections.abc
import types
import typing


def is_iterable(obj: typing.Any) -> bool:
    """Test if given object is an iterable object."""
    return (isinstance(obj, (list, tuple, types.GeneratorType))
            or (not isinstance(obj, (int, str, dict))
                and bool(getattr(obj, 'next', False))))


def is_dict_like(obj: typing.Any) -> bool:
    """Test if given object ``obj`` is an dict."""
    return isinstance(obj, (dict, collections.abc.Mapping))  # any others?


_LIST_LIKE_TYPES = (collections.abc.Iterable, collections.abc.Sequence)


def is_list_like(obj: typing.Any) -> bool:
    """Test if given object ``obj`` is a list or -like one."""
    return isinstance(obj, _LIST_LIKE_TYPES) and \
        not (isinstance(obj, str) or is_dict_like(obj))

# vim:sw=4:ts=4:et:
