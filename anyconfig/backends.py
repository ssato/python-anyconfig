#
# Copyright (C) 2011 - 2016 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Suppress:
# - false-positive warn at '... pkg_resources ...' line
# - import positions after some globals are defined
# pylint: disable=no-member,wrong-import-position
"""A module to aggregate config parser (loader/dumper) backends.
"""
from __future__ import absolute_import

import itertools
import logging
import operator
import pkg_resources

import anyconfig.compat
import anyconfig.utils

import anyconfig.backend.base
import anyconfig.backend.ini
import anyconfig.backend.json
import anyconfig.backend.properties
import anyconfig.backend.shellvars
import anyconfig.backend.xml

LOGGER = logging.getLogger(__name__)
PARSERS = [anyconfig.backend.ini.Parser, anyconfig.backend.json.Parser,
           anyconfig.backend.properties.Parser,
           anyconfig.backend.shellvars.Parser, anyconfig.backend.xml.Parser]

_NA_MSG = "%s is not available. Disabled %s support."

try:
    import anyconfig.backend.yaml
    PARSERS.append(anyconfig.backend.yaml.Parser)
except ImportError:
    LOGGER.info(_NA_MSG, "yaml module", "YAML")

try:
    import anyconfig.backend.configobj
    PARSERS.append(anyconfig.backend.configobj.Parser)
except ImportError:
    LOGGER.info(_NA_MSG, "ConfigObj module", "its")

try:
    import anyconfig.backend.msgpack
    PARSERS.append(anyconfig.backend.msgpack.Parser)
except ImportError:
    LOGGER.info(_NA_MSG, "msgpack module", "MessagePack")

try:
    import anyconfig.backend.toml
    PARSERS.append(anyconfig.backend.toml.Parser)
except ImportError:
    LOGGER.info(_NA_MSG, "toml module", "TOML")

try:
    import anyconfig.backend.bson
    PARSERS.append(anyconfig.backend.bson.Parser)
except ImportError:
    LOGGER.info(_NA_MSG, "bson module in pymongo package", "BSON")

for e in pkg_resources.iter_entry_points("anyconfig_backends"):
    try:
        PARSERS.append(e.load())
    except ImportError:
        continue


def fst(tpl):
    """
    >>> fst((0, 1))
    0
    """
    return tpl[0]


def snd(tpl):
    """
    >>> snd((0, 1))
    1
    """
    return tpl[1]


def groupby_key(itr, keyfunc):
    """
    An wrapper function around itertools.groupby

    :param itr: Iterable object, a list/tuple/genrator, etc.
    :param keyfunc: Key function to sort `itr`.

    >>> itr = [("a", 1), ("b", -1), ("c", 1)]
    >>> res = groupby_key(itr, operator.itemgetter(1))
    >>> [(key, tuple(grp)) for key, grp in res]
    [(-1, (('b', -1),)), (1, (('a', 1), ('c', 1)))]
    """
    return itertools.groupby(sorted(itr, key=keyfunc), key=keyfunc)


def uniq(iterable, **kwopts):
    """sorted + uniq

    .. note::
       sorted(set(iterable), key=iterable.index) cannot be used for any
       iterables (generator, a list of dicts, etc.), I guess.

    :param iterable: Iterable objects, a list, generator, iterator, etc.
    :param kwopts: Keyword options passed to sorted()
    :return: a sorted list of items in iterable

    >>> uniq([1, 2, 3, 1, 2])
    [1, 2, 3]
    >>> uniq((i for i in (2, 10, 3, 2, 5, 1, 7, 3)))
    [1, 2, 3, 5, 7, 10]
    >>> uniq(({str(i): i} for i in (2, 10, 3, 2, 5, 1, 7, 3)),
    ...      key=lambda d: int(list(d.keys())[0]))
    [{'1': 1}, {'2': 2}, {'3': 3}, {'5': 5}, {'7': 7}, {'10': 10}]
    """
    return [t[0] for t in itertools.groupby(sorted(iterable, **kwopts))]


def is_parser(obj):
    """
    :return: True if given `obj` is an instance of parser.

    >>> is_parser("ini")
    False
    >>> is_parser(anyconfig.backend.base.Parser)
    False
    >>> is_parser(anyconfig.backend.base.Parser())
    True
    """
    return isinstance(obj, anyconfig.backend.base.Parser)


def list_parsers_by_type(cps=None):
    """
    :return: List (generator) of (config_type, [config_parser])
    """
    if cps is None:
        cps = PARSERS

    return ((t, sorted(p, key=operator.methodcaller("priority"))) for t, p
            in groupby_key(cps, operator.methodcaller("type")))


def _list_xppairs(xps):
    """List config parsers by priority.
    """
    return sorted((snd(xp) for xp in xps),
                  key=operator.methodcaller("priority"))


def list_parsers_by_extension(cps=None):
    """
    :return: List (generator) of (config_ext, [config_parser])
    """
    if cps is None:
        cps = PARSERS

    cps_by_ext = anyconfig.utils.concat(([(x, p) for x in p.extensions()] for p
                                         in cps))

    return ((x, _list_xppairs(xps)) for x, xps in groupby_key(cps_by_ext, fst))


def find_by_file(path_or_stream, cps=None, is_path_=False):
    """
    Find config parser by the extension of file `path_or_stream`, file path or
    stream (a file or file-like objects).

    :param path_or_stream: Config file path or file/file-like object
    :param cps: A list of pairs :: (type, parser_class)
    :param is_path_: True if given `path_or_stream` is a file path

    :return: Config Parser class found

    >>> find_by_file("a.missing_cnf_ext") is None
    True
    >>> strm = anyconfig.compat.StringIO()
    >>> find_by_file(strm) is None
    True
    >>> find_by_file("a.json")
    <class 'anyconfig.backend.json.Parser'>
    >>> find_by_file("a.json", is_path_=True)
    <class 'anyconfig.backend.json.Parser'>
    """
    if cps is None:
        cps = PARSERS

    if not is_path_ and not anyconfig.utils.is_path(path_or_stream):
        path_or_stream = anyconfig.utils.get_path_from_stream(path_or_stream)
        if path_or_stream is None:
            return None  # There is no way to detect file path.

    ext_ref = anyconfig.utils.get_file_extension(path_or_stream)
    for ext, psrs in list_parsers_by_extension(cps):
        if ext == ext_ref:
            return psrs[-1]

    return None


def find_by_type(cptype, cps=None):
    """
    Find config parser by file's extension.

    :param cptype: Config file's type
    :param cps: A list of pairs :: (type, parser_class)
    :return: Config Parser class found

    >>> find_by_type("missing_type") is None
    True
    """
    if cps is None:
        cps = PARSERS

    for type_, psrs in list_parsers_by_type(cps):
        if type_ == cptype:
            return psrs[-1] or None

    return None


def find_parser(path_or_stream, forced_type=None, is_path_=False):
    """
    Find out config parser object appropriate to load from a file of given path
    or file/file-like object.

    :param path_or_stream: Configuration file path or file / file-like object
    :param forced_type: Forced configuration parser type
    :param is_path_: True if given `path_or_stream` is a file path

    :return: A tuple of (Parser class or None, "" or error message)

    >>> find_parser(None)
    Traceback (most recent call last):
    ValueError: path_or_stream or forced_type must be some value

    >>> find_parser(None, "ini")
    (<class 'anyconfig.backend.ini.Parser'>, '')
    >>> find_parser(None, "type_not_exist")
    (None, 'No parser found for given type: type_not_exist')

    >>> find_parser("cnf.json")
    (<class 'anyconfig.backend.json.Parser'>, '')
    >>> find_parser("cnf.json", is_path_=True)
    (<class 'anyconfig.backend.json.Parser'>, '')
    >>> find_parser("cnf.ext_not_found")
    (None, 'No parser found for given file: cnf.ext_not_found')
    """
    if not path_or_stream and forced_type is None:
        raise ValueError("path_or_stream or forced_type must be some value")

    err = ""
    if forced_type is not None:
        parser = find_by_type(forced_type)
        if parser is None:
            err = "No parser found for given type: %s" % forced_type
    else:
        parser = find_by_file(path_or_stream, is_path_=is_path_)
        if parser is None:
            err = "No parser found for given file: %s" % path_or_stream

    return (parser, err)


def list_types(cps=None):
    """List available config types.
    """
    if cps is None:
        cps = PARSERS

    return uniq(t for t, ps in list_parsers_by_type(cps))

# vim:sw=4:ts=4:et:
