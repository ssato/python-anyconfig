#
# Copyright (C) 2011 - 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Suppress:
# - false-positive warn at '... pkg_resources ...' line
# - import positions after some globals are defined
# pylint: disable=no-member,wrong-import-position
"""A module to aggregate config parser (loader/dumper) backends.
"""
from __future__ import absolute_import

import logging

import anyconfig.compat
import anyconfig.ioinfo
import anyconfig.processors
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
    import anyconfig.backend.toml
    PARSERS.append(anyconfig.backend.toml.Parser)
except ImportError:
    LOGGER.info(_NA_MSG, "toml module", "TOML")

PARSERS.extend(anyconfig.processors.load_plugins("anyconfig_backends"))


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


def inspect_io_obj(obj, prs=None, forced_type=None):
    """
    Inspect a given object `obj` which may be a path string, file / file-like
    object, pathlib.Path object or `~anyconfig.globals.IOInfo` namedtuple
    object, and find out appropriate parser object to load or dump from/to it
    along with other I/O information.

    :param obj:
        a file path string, file / file-like object, pathlib.Path object or
        `~anyconfig.globals.IOInfo` object
    :param prs: A list of parser classes
    :param forced_type: Forced type of parser to load or dump

    :return: anyconfig.globals.IOInfo object :: namedtuple
    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    if prs is None:
        prs = PARSERS

    return anyconfig.ioinfo.make(obj, prs, forced_type=forced_type)


def find_parser_by_type(forced_type, prs=None):
    """
    Find out appropriate parser object to load inputs of given type.

    :param forced_type: Forced parser type
    :param prs: A list of parser classes

    :return:
        An instance of :class:`~anyconfig.backend.base.Parser` or None means no
        appropriate parser was found
    :raises: UnknownProcessorTypeError
    """
    if forced_type is None or not forced_type:
        raise ValueError("forced_type must be a some string")

    if isinstance(forced_type, anyconfig.backend.base.Parser):
        return forced_type

    if prs is None:
        prs = PARSERS

    return anyconfig.processors.find_by_type(forced_type, prs)()


def find_parser(obj, prs=None, forced_type=None):
    """
    Find out appropriate parser object to load from a file of given path or
    file/file-like object.

    :param obj:
        a file path string, file / file-like object, pathlib.Path object or
        `~anyconfig.globals.IOInfo` object
    :param forced_type: Forced configuration parser type

    :return: A tuple of (Parser class or None, "" or error message)
    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    if anyconfig.utils.is_ioinfo(obj):
        return obj.processor  # It must have this.

    ioi = inspect_io_obj(obj, prs, forced_type)
    psr = ioi.processor
    LOGGER.debug("Using parser %r [%s][I/O: %s]", psr, psr.type(), ioi.type)
    return psr


def list_types(cps=None):
    """List available types parsers support.
    """
    if cps is None:
        cps = PARSERS

    return sorted(set(p.type() for p in cps))

# vim:sw=4:ts=4:et:
