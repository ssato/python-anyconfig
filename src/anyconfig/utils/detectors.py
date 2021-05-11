#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Functions to detect something.
"""
import collections.abc
import pathlib
import types
import typing

from ..common import (
    IOInfo, IOI_KEYS, IOI_STREAM
)


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
    >>> is_iterable("abc")
    False
    >>> is_iterable(0)
    False
    >>> is_iterable({})
    False
    """
    return isinstance(obj, (list, tuple, types.GeneratorType)) or \
        (not isinstance(obj, (int, str, dict)) and
         bool(getattr(obj, "next", False)))


def is_path(obj: typing.Any) -> bool:
    """
    Is given object 'obj' a file path?

    :param obj: file path or something
    :return: True if 'obj' is a file path
    """
    return isinstance(obj, str)


def is_path_obj(obj: typing.Any) -> bool:
    """Is given object 'input' a pathlib.Path object?

    :param obj: a pathlib.Path object or something
    :return: True if 'obj' is a pathlib.Path object

    >>> obj = pathlib.Path(__file__)
    >>> assert is_path_obj(obj)
    >>> assert not is_path_obj(__file__)
    """
    return isinstance(obj, pathlib.Path)


def is_file_stream(obj: typing.Any) -> bool:
    """Is given object 'input' a file stream (file/file-like object)?

    :param obj: a file / file-like (stream) object or something
    :return: True if 'obj' is a file stream

    >>> assert is_file_stream(open(__file__))
    >>> assert not is_file_stream(__file__)
    """
    return callable(getattr(obj, 'read', False))


def is_ioinfo(obj: typing.Any) -> bool:
    """
    :return: True if given 'obj' is a 'IOInfo' namedtuple object.

    >>> assert not is_ioinfo(1)
    >>> assert not is_ioinfo("aaa")
    >>> assert not is_ioinfo({})
    >>> assert not is_ioinfo(('a', 1, {}))

    >>> from ..common import IOI_PATH_STR
    >>> inp = IOInfo("/etc/hosts", IOI_PATH_STR, "/etc/hosts", None)
    >>> assert is_ioinfo(inp)
    """
    if isinstance(obj, tuple) and getattr(obj, '_asdict', False):
        return all(k in typing.cast(IOInfo, obj)._asdict() for k in IOI_KEYS)

    return False


def is_stream_ioinfo(obj: typing.Any) -> bool:
    """
    :param obj: IOInfo object or something
    :return: True if given IOInfo object 'obj' is of file / file-like object

    >>> ioi = IOInfo(None, IOI_STREAM, None, None)
    >>> assert is_stream_ioinfo(ioi)
    >>> assert not is_stream_ioinfo(__file__)
    """
    return getattr(obj, "type", None) == IOI_STREAM


def is_path_like_object(obj: typing.Any, marker: str = GLOB_MARKER) -> bool:
    """
    Is given object 'obj' a path string, a pathlib.Path, a file / file-like
    (stream) or IOInfo namedtuple object?

    :param obj:
        a path string, pathlib.Path object, a file / file-like or 'IOInfo'
        object

    :return:
        True if 'obj' is a path string or a pathlib.Path object or a file
        (stream) object

    >>> assert is_path_like_object(__file__)
    >>> assert not is_path_like_object("/a/b/c/*.json", '*')

    >>> assert is_path_like_object(pathlib.Path("a.ini"))
    >>> assert not is_path_like_object(pathlib.Path("x.ini"), 'x')
    >>> assert is_path_like_object(open(__file__))
    """
    return ((is_path(obj) and marker not in obj) or
            (is_path_obj(obj) and marker not in obj.as_posix()) or
            is_file_stream(obj) or is_ioinfo(obj))


def is_dict_like(obj: typing.Any) -> bool:
    """
    :param obj: Any object behaves like a dict.

    >>> is_dict_like("a string")
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
    >>> is_list_like("abc")
    False
    >>> is_list_like(0)
    False
    >>> is_list_like({})
    False
    """
    return isinstance(obj, _LIST_LIKE_TYPES) and \
        not (isinstance(obj, str) or is_dict_like(obj))


def is_paths(maybe_paths: typing.Any, marker: str = '*') -> bool:
    """
    Does given object 'maybe_paths' consist of path or path pattern strings?
    """
    if is_file_stream(maybe_paths) or is_ioinfo(maybe_paths):
        return False

    return (
        (is_path(maybe_paths) and marker in maybe_paths) or  # Path str
        (is_path_obj(maybe_paths) and marker in str(maybe_paths)) or
        (is_list_like(maybe_paths) and
         all(
            is_path(p) or is_ioinfo(p) or is_path_obj(p) or is_file_stream(p)
            for p in maybe_paths)
         )
    )

# vim:sw=4:ts=4:et:
