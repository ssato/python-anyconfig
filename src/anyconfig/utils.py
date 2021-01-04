#
# Copyright (C) 2012 - 2018 Satoru SATOH <ssato@redhat.com>
# Copyright (C) 2019 - 2020 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Misc utility routines for anyconfig module.
"""
from __future__ import absolute_import

import collections.abc
import functools
import itertools
import os.path
import os
import re
import pathlib
import types
import typing

import anyconfig.globals


def groupby(itr, key_fn=None):
    """
    An wrapper function around itertools.groupby to sort each results.

    :param itr: Iterable object, a list/tuple/genrator, etc.
    :param key_fn: Key function to sort 'itr'.

    >>> import operator
    >>> itr = [("a", 1), ("b", -1), ("c", 1)]
    >>> res = groupby(itr, operator.itemgetter(1))
    >>> [(key, tuple(grp)) for key, grp in res]
    [(-1, (('b', -1),)), (1, (('a', 1), ('c', 1)))]
    """
    return itertools.groupby(sorted(itr, key=key_fn), key=key_fn)


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

    return ""


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
    return list(itertools.chain.from_iterable(xs for xs in xss))


def is_path(obj):
    """
    Is given object 'obj' a file path?

    :param obj: file path or something
    :return: True if 'obj' is a file path
    """
    return isinstance(obj, str)


def is_path_obj(obj):
    """Is given object 'input' a pathlib.Path object?

    :param obj: a pathlib.Path object or something
    :return: True if 'obj' is a pathlib.Path object

    >>> obj = pathlib.Path(__file__)
    >>> assert is_path_obj(obj)
    >>> assert not is_path_obj(__file__)
    """
    return isinstance(obj, pathlib.Path)


def is_file_stream(obj):
    """Is given object 'input' a file stream (file/file-like object)?

    :param obj: a file / file-like (stream) object or something
    :return: True if 'obj' is a file stream

    >>> assert is_file_stream(open(__file__))
    >>> assert not is_file_stream(__file__)
    """
    return getattr(obj, "read", False)


def is_ioinfo(obj, keys=None):
    """
    :return: True if given 'obj' is a 'IOInfo' namedtuple object.

    >>> assert not is_ioinfo(1)
    >>> assert not is_ioinfo("aaa")
    >>> assert not is_ioinfo({})
    >>> assert not is_ioinfo(('a', 1, {}))

    >>> inp = anyconfig.globals.IOInfo("/etc/hosts",
    ...                                anyconfig.globals.IOI_PATH_STR,
    ...                                "/etc/hosts", None)
    >>> assert is_ioinfo(inp)
    """
    if keys is None:
        keys = anyconfig.globals.IOI_KEYS

    if isinstance(obj, tuple) and getattr(obj, "_asdict", False):
        return all(k in obj._asdict() for k in keys)

    return False


def is_stream_ioinfo(obj):
    """
    :param obj: IOInfo object or something
    :return: True if given IOInfo object 'obj' is of file / file-like object

    >>> ioi = anyconfig.globals.IOInfo(None, anyconfig.globals.IOI_STREAM,
    ...                                None, None)
    >>> assert is_stream_ioinfo(ioi)
    >>> assert not is_stream_ioinfo(__file__)
    """
    return getattr(obj, "type", None) == anyconfig.globals.IOI_STREAM


def is_path_like_object(obj, marker='*'):
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


def is_paths(maybe_paths, marker='*'):
    """
    Does given object 'maybe_paths' consist of path or path pattern strings?
    """
    return ((is_path(maybe_paths) and marker in maybe_paths) or  # Path str
            (is_path_obj(maybe_paths) and marker in maybe_paths.as_posix()) or
            (is_iterable(maybe_paths) and
             all(is_path(p) or is_ioinfo(p) or is_path_obj(p)
                 for p in maybe_paths)))


def get_path_from_stream(strm: typing.IO, safe: bool = False
                         ) -> typing.Optional[str]:
    """
    Try to get file path from given file or file-like object 'strm'.

    :param strm: A file or file-like object might have its file path info
    :return: file path or None
    :raises: ValueError
    """
    if not is_file_stream(strm) and not safe:
        raise ValueError("Given object does not look a file/file-like "
                         "object: %r" % strm)

    path = getattr(strm, "name", None)
    if path is not None:
        try:
            return str(pathlib.Path(path).resolve())
        except (TypeError, ValueError):
            pass

    return None


@functools.lru_cache()
def split_re(marker: str, sep: str = os.path.sep) -> typing.Pattern:
    """Generate a regexp pattern object to split path by marker.
    """
    return re.compile(r'([^{0}]+){1}(.*\{0}.*)'.format(marker, sep))


def split_path_by_marker(path: str, marker: str = '*',
                         sep: str = os.path.sep
                         ) -> typing.Tuple[typing.Optional[str],
                                           typing.Optional[str]]:
    """
    Split given path string by the marker.

    >>> split_path_by_marker('a.txt')
    ('a.txt', None)
    >>> split_path_by_marker('*.txt')
    (None, '*.txt')
    >>> split_path_by_marker('a/*.txt')
    ('a', '*.txt')
    >>> split_path_by_marker('a/b/*.txt')
    ('a/b', '*.txt')
    >>> split_path_by_marker('a/b/*/*.txt')
    ('a/b', '*/*.txt')
    """
    if marker not in path:
        return (path, None)

    if sep not in path:
        return (None, path)

    return split_re(marker, sep=sep).match(path).groups()


PathOrIO = typing.Union[pathlib.Path, typing.IO]


def expand_paths_itr(paths: typing.Union[str, pathlib.Path,
                                         typing.Tuple, typing.IO],
                     marker: str = '*'
                     ) -> typing.Iterator[PathOrIO]:
    """
    :param paths:
        A glob path pattern string or pathlib.Path object holding such path, or
        a list consists of path strings or glob path pattern strings or
        pathlib.Path object holding such ones.

    :param marker: A character or string to globbing paths
    """
    if isinstance(paths, (str, pathlib.Path)):
        if isinstance(paths, pathlib.Path):
            paths = str(paths)

        (base, pattern) = split_path_by_marker(paths, marker=marker)

        if pattern is None:
            yield pathlib.Path(base)
            return

        base = pathlib.Path(os.curdir if base is None else base).resolve()
        for path in sorted(base.glob(pattern)):
            yield path

    elif is_file_stream(paths):
        yield paths

    elif is_ioinfo(paths):
        yield pathlib.Path(paths.path)

    else:
        for path in paths:
            for cpath in expand_paths_itr(path, marker=marker):
                yield cpath


def maybe_path_key(obj: typing.Union[pathlib.Path, typing.IO]
                   ) -> typing.Union[pathlib.Path, str, int]:
    """
    Key function for maybe path object :: str | pathlib.Path | Tuple | IO
    """
    if is_file_stream(obj):
        return getattr(obj, "name", id(obj))

    return obj


def expand_paths(paths: typing.Union[str, pathlib.Path,
                                     typing.Tuple, typing.IO],
                 marker: str = '*'
                 ) -> typing.Iterable[typing.Union[pathlib.Path, typing.IO]]:
    """
    :param paths:
        A glob path pattern string or pathlib.Path object holding such path, or
        a list consists of path strings or glob path pattern strings or
        pathlib.Path object holding such ones, or file objects
    :param marker: Glob marker character or string, e.g. '*'
    """
    return sorted(expand_paths_itr(paths, marker=marker), key=maybe_path_key)


def _try_to_get_extension(obj: PathOrIO) -> typing.Optional[str]:
    """
    Try to get file extension from given path or file object.

    :param obj: a file, file-like object or something
    :return: File extension or None

    >>> path = pathlib.Path(__file__)
    >>> _try_to_get_extension(path)
    'py'
    >>> with path.open() as fio:
    ...     _try_to_get_extension(fio)
    'py'
    """
    if isinstance(obj, pathlib.Path):
        return obj.suffix[1:]

    path = get_path_from_stream(obj, safe=True)
    if path is None:
        return None

    return _try_to_get_extension(pathlib.Path(path))


def are_same_file_types(objs: typing.List[PathOrIO]) -> bool:
    """
    Are given objects, pathlib.Path or io, same type (have same extension)?
    """
    if not objs:
        return False

    ext = _try_to_get_extension(objs[0])
    if ext is None:
        return False

    return all(_try_to_get_extension(p) == ext for p in objs[1:])


def noop(val, *_args, **_kwargs):
    """A function does nothing.

    >>> noop(1)
    1
    """
    # It means nothing but can suppress 'Unused argument' pylint warns.
    # (val, args, kwargs)[0]
    return val


_LIST_LIKE_TYPES = (collections.abc.Iterable, collections.abc.Sequence)


def is_dict_like(obj):
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


def is_namedtuple(obj):
    """
    >>> import collections
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
        not (isinstance(obj, str) or is_dict_like(obj))


def filter_options(keys, options):
    """
    Filter 'options' with given 'keys'.

    :param keys: key names of optional keyword arguments
    :param options: optional keyword arguments to filter with 'keys'

    >>> filter_options(("aaa", ), dict(aaa=1, bbb=2))
    {'aaa': 1}
    >>> filter_options(("aaa", ), dict(bbb=2))
    {}
    """
    return dict((k, options[k]) for k in keys if k in options)


def memoize(fnc):
    """memoization function.

    >>> import random
    >>> imax = 100
    >>> def fnc1(arg=True):
    ...     return arg and random.choice((True, False))
    >>> fnc2 = memoize(fnc1)
    >>> (ret1, ret2) = (fnc1(), fnc2())
    >>> assert any(fnc1() != ret1 for i in range(imax))
    >>> assert all(fnc2() == ret2 for i in range(imax))
    """
    cache = dict()

    @functools.wraps(fnc)
    def wrapped(*args, **kwargs):
        """Decorated one"""
        key = repr(args) + repr(kwargs)
        if key not in cache:
            cache[key] = fnc(*args, **kwargs)

        return cache[key]

    return wrapped

# vim:sw=4:ts=4:et:
