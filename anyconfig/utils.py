#
# Copyright (C) 2012 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""Misc utility routines for anyconfig module.
"""
from __future__ import absolute_import

import collections
import glob
import os.path
import types

import anyconfig.compat


def get_file_extension(file_path):
    """
    >>> get_file_extension("/a/b/c")
    ''
    >>> get_file_extension("/a/b.txt")
    'txt'
    >>> get_file_extension("/a/b/c.tar.xz")
    'xz'
    """
    _ext = os.path.splitext(file_path)[-1]
    if _ext:
        return _ext[1:] if _ext.startswith('.') else _ext
    else:
        return ""


def sglob(files_pattern):
    """
    glob.glob alternative of which results sorted always.
    """
    return sorted(glob.glob(files_pattern))


def is_iterable(obj):
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


def concat(xss):
    """
    Concatenates a list of lists.

    >>> concat([[]])
    []
    >>> concat((()))
    []
    >>> concat([[1,2,3],[4,5]])
    [1, 2, 3, 4, 5]
    >>> concat([[1,2,3],[4,5,[6,7]]])
    [1, 2, 3, 4, 5, [6, 7]]
    >>> concat(((1,2,3),(4,5,[6,7])))
    [1, 2, 3, 4, 5, [6, 7]]
    >>> concat(((1,2,3),(4,5,[6,7])))
    [1, 2, 3, 4, 5, [6, 7]]
    >>> concat((i, i*2) for i in range(3))
    [0, 0, 1, 2, 2, 4]
    """
    return list(anyconfig.compat.from_iterable(xs for xs in xss))


def normpath(path):
    """Normalize path.

    - eliminating double slashes, etc. (os.path.normpath)
    - ensure paths contain ~[user]/ expanded.

    :param path: Path string :: str
    """
    return os.path.normpath(os.path.expanduser(path) if '~' in path else path)


def is_path(path_or_stream):
    """
    Is given object `path_or_stream` a file path?

    :param path_or_stream: file path or stream, file/file-like object
    :return: True if `path_or_stream` is a file path
    """
    return isinstance(path_or_stream, anyconfig.compat.STR_TYPES)


def get_path_from_stream(maybe_stream):
    """
    Try to get file path from given stream `stream`.

    :param maybe_stream: A file or file-like object
    :return: Path of given file or file-like object or None

    >>> __file__ == get_path_from_stream(__file__)
    True
    >>> __file__ == get_path_from_stream(open(__file__, 'r'))
    True
    >>> strm = anyconfig.compat.StringIO()
    >>> get_path_from_stream(strm) is None
    True
    """
    if is_path(maybe_stream):
        return maybe_stream  # It's path.

    maybe_path = getattr(maybe_stream, "name", None)
    if maybe_path is not None:
        maybe_path = os.path.abspath(maybe_path)

    return maybe_path


def _try_to_get_extension(path_or_strm):
    """
    Try to get file extension from given path or file object.

    :return: File extension or None
    """
    path = get_path_from_stream(path_or_strm)
    if path is None:
        return None

    return get_file_extension(path) or None


def are_same_file_types(paths):
    """
    Are given (maybe) file paths same type (extension) ?

    :param paths: A list of file path or file(-like) objects

    >>> are_same_file_types([])
    False
    >>> are_same_file_types(["a.conf"])
    True
    >>> are_same_file_types(["a.conf", "b.conf"])
    True
    >>> are_same_file_types(["a.yml", "b.yml"])
    True
    >>> are_same_file_types(["a.yml", "b.json"])
    False
    >>> strm = anyconfig.compat.StringIO()
    >>> are_same_file_types(["a.yml", "b.yml", strm])
    False
    """
    if not paths:
        return False

    ext = _try_to_get_extension(paths[0])
    if ext is None:
        return False

    return all(_try_to_get_extension(p) == ext for p in paths[1:])


def _norm_paths_itr(paths, marker='*'):
    """Iterator version of :func:`norm_paths`.
    """
    for path in paths:
        if is_path(path):
            if marker in path:  # glob path pattern
                for ppath in sglob(path):
                    yield ppath
            else:
                yield path  # a simple file path
        else:  # A file or file-like object
            yield path


def norm_paths(paths, marker='*'):
    """
    :param paths:
        A glob path pattern string, or a list consists of path strings or glob
        path pattern strings or file objects
    :param marker: Glob marker character or string, e.g. '*'
    :return: List of path strings

    >>> norm_paths([])
    []
    >>> norm_paths("/usr/lib/a/b.conf /etc/a/b.conf /run/a/b.conf".split())
    ['/usr/lib/a/b.conf', '/etc/a/b.conf', '/run/a/b.conf']
    >>> paths_s = os.path.join(os.path.dirname(__file__), "u*.py")
    >>> ref = sglob(paths_s)
    >>> assert norm_paths(paths_s) == ref
    >>> ref = ["/etc/a.conf"] + ref
    >>> assert norm_paths(["/etc/a.conf", paths_s]) == ref
    >>> strm = anyconfig.compat.StringIO()
    >>> assert norm_paths(["/etc/a.conf", strm]) == ["/etc/a.conf", strm]
    """
    if is_path(paths) and marker in paths:
        return sglob(paths)

    return list(_norm_paths_itr(paths, marker=marker))


# pylint: disable=unused-argument
def noop(val, *args, **kwargs):
    """A function does nothing.

    >>> noop(1)
    1
    """
    # It means nothing but can suppress 'Unused argument' pylint warns.
    # (val, args, kwargs)[0]
    return val


_LIST_LIKE_TYPES = (collections.Iterable, collections.Sequence)


def is_dict_like(obj):
    """
    :param obj: Any object behaves like a dict.

    >>> is_dict_like("a string")
    False
    >>> is_dict_like({})
    True
    >>> is_dict_like(anyconfig.compat.OrderedDict((('a', 1), ('b', 2))))
    True
    """
    return isinstance(obj, (dict, collections.Mapping))  # any others?


def is_namedtuple(obj):
    """
    >>> p0 = collections.namedtuple("Point", "x y")(1, 2)
    >>> is_namedtuple(p0)
    True
    >>> is_namedtuple(tuple(p0))
    False
    """
    return isinstance(obj, tuple) and hasattr(obj, "_asdict")


def is_list_like(obj):
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
        not (isinstance(obj, anyconfig.compat.STR_TYPES) or is_dict_like(obj))


def filter_options(keys, options):
    """
    Filter `options` with given `keys`.

    :param keys: key names of optional keyword arguments
    :param options: optional keyword arguments to filter with `keys`

    >>> filter_options(("aaa", ), dict(aaa=1, bbb=2))
    {'aaa': 1}
    >>> filter_options(("aaa", ), dict(bbb=2))
    {}
    """
    return dict((k, options[k]) for k in keys if k in options)

# vim:sw=4:ts=4:et:
