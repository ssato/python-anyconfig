#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
#  pylint: disable=deprecated-method
r"""INI backend:

- Format to support: INI or INI like ones
- Requirements: The following standard module which should be available always.

  - ConfigParser in python 2 standard library:
    https://docs.python.org/2.7/library/configparser.html

  - configparser in python 3 standard library:
    https://docs.python.org/3/library/configparser.html

- Development Status :: 4 - Beta
- Limitations: It cannot process nested configuration dicts correctly due to
  the limitation of the module and the format ifself.

- Special options:

  - Use 'ac_parse_value' boolean keyword option if you want to parse values by
    custom parser, anyconfig.backend.ini._parse.

Changelog:

.. versionchanged:: 0.3

   - Introduce 'ac_parse_value' keyword option to switch behaviors, same as
     original configparser and rich backend parsing each parameter values.
"""
import configparser
import os
import typing

from ..parser import parse, parse_list
from ..utils import (
    filter_options, is_iterable, noop
)
from . import base


_SEP = ','
try:
    DEFAULTSECT: str = configparser.DEFAULTSECT
except AttributeError:
    DEFAULTSECT: str = 'DEFAULT'  # type: ignore


def _parse(val_s: str, sep: str = _SEP):
    """
    FIXME: May be too naive implementation.

    :param val_s: A string represents some value to parse
    :param sep: separator between values

    >>> _parse(r'"foo string"')
    'foo string'
    >>> _parse("a, b, c")
    ['a', 'b', 'c']
    >>> _parse("aaa")
    'aaa'
    """
    if (val_s.startswith('"') and val_s.endswith('"')) or \
            (val_s.startswith("'") and val_s.endswith("'")):
        return val_s[1:-1]
    if sep in val_s:
        return [parse(typing.cast(str, x)) for x in parse_list(val_s)]

    return parse(val_s)


def _to_s(val: typing.Any, sep: str = ', ') -> str:
    """Convert any to string.

    :param val: An object
    :param sep: separator between values

    >>> _to_s([1, 2, 3])
    '1, 2, 3'
    >>> _to_s("aaa")
    'aaa'
    """
    if is_iterable(val):
        return sep.join(str(x) for x in val)

    return str(val)


def _parsed_items(items: typing.Iterable[typing.Tuple[str, typing.Any]],
                  sep: str = _SEP, **options
                  ) -> typing.Iterator[typing.Tuple[str, typing.Any]]:
    """
    :param items: List of pairs, [(key, value)], or generator yields pairs
    :param sep: Seprator string
    :return: Generator to yield (key, value) pair of 'dic'
    """
    parse = _parse if options.get("ac_parse_value") else noop
    for key, val in items:
        yield (key, parse(val, sep))  # type: ignore


def _make_parser(**kwargs):
    """
    :return: (keyword args to be used, parser object)
    """
    # Optional arguements for configparser.SafeConfigParser{,readfp}
    kwargs_0 = filter_options(
        ("defaults", "dict_type", "allow_no_value"), kwargs
    )
    kwargs_1 = filter_options(("filename", ), kwargs)

    try:
        psr = configparser.SafeConfigParser(**kwargs_0)
    except TypeError:
        # .. note::
        #    It seems ConfigParser.*ConfigParser in python 2.6 does not support
        #    'allow_no_value' option parameter, and TypeError will be thrown.
        kwargs_0 = filter_options(("defaults", "dict_type"), kwargs)
        psr = configparser.SafeConfigParser(**kwargs_0)

    return (kwargs_1, psr)


def _load(stream, container, sep=_SEP, dkey=DEFAULTSECT, **kwargs):
    """
    :param stream: File or file-like object provides ini-style conf
    :param container: any callable to make container
    :param sep: Seprator string
    :param dkey: Default section name

    :return: Dict or dict-like object represents config values
    """
    (kwargs_1, psr) = _make_parser(**kwargs)
    psr.read_file(stream, **kwargs_1)

    cnf = container()
    kwargs["sep"] = sep

    defaults = psr.defaults()
    if defaults:
        cnf[dkey] = container(_parsed_items(defaults.items(), **kwargs))

    for sect in psr.sections():
        cnf[sect] = container(_parsed_items(psr.items(sect), **kwargs))

    return cnf


def _dumps_itr(cnf: typing.Dict[str, typing.Any],
               dkey: str = DEFAULTSECT):
    """
    :param cnf: Configuration data to dump
    """
    for sect, params in cnf.items():
        yield "[%s]" % sect

        for key, val in params.items():
            if sect != dkey and dkey in cnf and cnf[dkey].get(key) == val:
                continue  # It should be in [DEFAULT] section.

            yield "%s = %s" % (key, _to_s(val))

        yield ''  # it will be a separator between each sections.


def _dumps(cnf: typing.Dict[str, typing.Any], **_kwargs) -> str:
    """
    :param cnf: Configuration data to dump
    :param _kwargs: optional keyword parameters to be sanitized :: dict

    :return: String representation of 'cnf' object in INI format
    """
    return os.linesep.join(line for line in _dumps_itr(cnf))


class Parser(base.Parser, base.FromStreamLoaderMixin,
             base.ToStringDumperMixin):
    """
    Ini config files parser.
    """
    _cid: str = 'ini'
    _type: str = 'ini'
    _extensions: typing.List[str] = ['ini']
    _load_opts: typing.List[str] = [
        "defaults", "dict_type", "allow_no_value", "filename", "ac_parse_value"
    ]
    _dict_opts: typing.List[str] = ["dict_type"]

    dump_to_string = base.to_method(_dumps)
    load_from_stream = base.to_method(_load)

# vim:sw=4:ts=4:et:
