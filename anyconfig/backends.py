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
import anyconfig.backend.pickle
import anyconfig.backend.properties
import anyconfig.backend.shellvars
import anyconfig.backend.xml

LOGGER = logging.getLogger(__name__)
PARSERS = [anyconfig.backend.ini.Parser, anyconfig.backend.json.Parser,
           anyconfig.backend.pickle.Parser,
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

try:
    import anyconfig.backend.cbor
    PARSERS.append(anyconfig.backend.cbor.Parser)
except ImportError:
    LOGGER.info(_NA_MSG, "cbor module in cbor package", "CBOR")

for e in pkg_resources.iter_entry_points("anyconfig_backends"):
    try:
        PARSERS.append(e.load())
    except ImportError:
        continue


class UnknownParserTypeError(RuntimeError):
    """Raise if no parsers were found for given type."""
    def __init__(self, forced_type):
        msg = "No parser found for type '%s'" % forced_type
        super(UnknownParserTypeError, self).__init__(msg)


class UnknownFileTypeError(RuntimeError):
    """Raise if not parsers were found for given file path."""
    def __init__(self, path):
        msg = "No parser found for file '%s'" % path
        super(UnknownFileTypeError, self).__init__(msg)


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


def _list_parsers_by_type(cps):
    """
    :param cps: A list of parser classes
    :return: List (generator) of (config_type, [config_parser])
    """
    return ((t, sorted(p, key=operator.methodcaller("priority"))) for t, p
            in groupby_key(cps, operator.methodcaller("type")))


def _list_xppairs(xps):
    """List config parsers by priority.
    """
    return sorted((snd(xp) for xp in xps),
                  key=operator.methodcaller("priority"))


def _list_parsers_by_extension(cps):
    """
    :param cps: A list of parser classes
    :return: List (generator) of (config_ext, [config_parser])
    """
    cps_by_ext = anyconfig.utils.concat(([(x, p) for x in p.extensions()] for p
                                         in cps))

    return ((x, _list_xppairs(xps)) for x, xps in groupby_key(cps_by_ext, fst))


_PARSERS_BY_TYPE = tuple(_list_parsers_by_type(PARSERS))
_PARSERS_BY_EXT = tuple(_list_parsers_by_extension(PARSERS))


def find_by_file(path_or_stream, cps=_PARSERS_BY_EXT, is_path_=False):
    """
    Find config parser by the extension of file `path_or_stream`, file path or
    stream (a file or file-like objects).

    :param path_or_stream: Config file path or file/file-like object
    :param cps:
        A tuple of pairs of (type, parser_class) or None if you want to compute
        this value dynamically.
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
        cps = _list_parsers_by_extension(PARSERS)

    if not is_path_ and not anyconfig.utils.is_path(path_or_stream):
        path_or_stream = anyconfig.utils.get_path_from_stream(path_or_stream)
        if path_or_stream is None:
            return None  # There is no way to detect file path.

    ext_ref = anyconfig.utils.get_file_extension(path_or_stream)
    return next((psrs[-1] for ext, psrs in cps if ext == ext_ref), None)


def find_by_type(cptype, cps=_PARSERS_BY_TYPE):
    """
    Find config parser by file's extension.

    :param cptype: Config file's type
    :param cps:
        A list of pairs (type, parser_class) or None if you want to compute
        this value dynamically.

    :return: Config Parser class found

    >>> find_by_type("missing_type") is None
    True
    """
    if cps is None:
        cps = _list_parsers_by_type(PARSERS)

    return next((psrs[-1] or None for t, psrs in cps if t == cptype), None)


def find_parser(path_or_stream, forced_type=None, is_path_=False):
    """
    Find out config parser object appropriate to load from a file of given path
    or file/file-like object.

    :param path_or_stream: Configuration file path or file / file-like object
    :param forced_type: Forced configuration parser type
    :param is_path_: True if given `path_or_stream` is a file path

    :return: A tuple of (Parser class or None, "" or error message)

    >>> find_parser(None)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: path_or_stream or forced_type must be some value
    >>> find_parser(None, "type_not_exist"
    ...             )  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    UnknownParserTypeError: No parser found for type 'type_not_exist'
    >>> find_parser("cnf.ext_not_found"
    ...             )  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    UnknownFileTypeError: No parser found for file 'cnf.ext_not_found'

    >>> find_parser(None, "ini")
    <class 'anyconfig.backend.ini.Parser'>
    >>> find_parser("cnf.json")
    <class 'anyconfig.backend.json.Parser'>
    >>> find_parser("cnf.json", is_path_=True)
    <class 'anyconfig.backend.json.Parser'>
    """
    if not path_or_stream and forced_type is None:
        raise ValueError("path_or_stream or forced_type must be some value")

    if forced_type is not None:
        parser = find_by_type(forced_type)
        if parser is None:
            raise UnknownParserTypeError(forced_type)
    else:
        parser = find_by_file(path_or_stream, is_path_=is_path_)
        if parser is None:
            raise UnknownFileTypeError(path_or_stream)

    return parser


def list_types(cps=_PARSERS_BY_TYPE):
    """List available config types.
    """
    if cps is None:
        cps = _list_parsers_by_type(PARSERS)

    return sorted(set(next(anyconfig.compat.izip(*cps))))

# vim:sw=4:ts=4:et:
