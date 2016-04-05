#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
#  pylint: disable=unused-argument
"""INI or INI like config files backend.

.. versionchanged:: 0.3
   Introduce 'ac_parse_value' keyword option to switch behaviors, same as
   original configparser and rich backend parsing each parameter values.

- Format to support: INI or INI like ones
- Requirements: It should be available always.

  - ConfigParser in python 2 standard library:
    https://docs.python.org/2.7/library/configparser.html

  - configparser in python 3 standard library:
    https://docs.python.org/3/library/configparser.html

- Limitations: None obvious
- Special options:

  - Use 'ac_parse_value' boolean keyword option if you want to parse values by
    custom parser, anyconfig.backend.ini._parse.
"""
from __future__ import absolute_import

import anyconfig.backend.base
import anyconfig.parser as P
import anyconfig.utils

from anyconfig.compat import configparser, iteritems
from anyconfig.backend.base import mk_opt_args


_SEP = ','


def _noop(val, *args, **kwargs):
    """
    Parser does nothing.
    """
    # It means nothing but can suppress 'Unused argument' pylint warns.
    # (val, args, kwargs)[0]
    return val


def _parse(val_s, sep=_SEP):
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
    elif sep in val_s:
        return [P.parse(x) for x in P.parse_list(val_s)]
    else:
        return P.parse(val_s)


def _to_s(val, sep=", "):
    """Convert any to string.

    :param val: An object
    :param sep: separator between values

    >>> _to_s([1, 2, 3])
    '1, 2, 3'
    >>> _to_s("aaa")
    'aaa'
    """
    if anyconfig.utils.is_iterable(val):
        return sep.join(str(x) for x in val)
    else:
        return str(val)


def _load(stream, to_container=dict, sep=_SEP, **kwargs):
    """
    :param stream: File or file-like object provides ini-style conf
    :param to_container: any callable to make container
    :param sep: Seprator string

    :return: Dict or dict-like object represents config values
    """
    _parse_val = _parse if kwargs.get("ac_parse_value", False) else _noop

    # Optional arguements for configparser.SafeConfigParser{,readfp}
    kwargs_0 = mk_opt_args(("defaults", "dict_type", "allow_no_value"), kwargs)
    kwargs_1 = mk_opt_args(("filename", ), kwargs)

    try:
        parser = configparser.SafeConfigParser(**kwargs_0)
    except TypeError:
        # .. note::
        #    It seems ConfigPaser.*ConfigParser in python 2.6 does not support
        #    'allow_no_value' option parameter, and TypeError will be thrown.
        kwargs_0 = mk_opt_args(("defaults", "dict_type"), kwargs)
        parser = configparser.SafeConfigParser(**kwargs_0)

    cnf = to_container()
    parser.readfp(stream, **kwargs_1)

    # .. note:: Process DEFAULT config parameters as special ones.
    defaults = parser.defaults()
    if defaults:
        cnf["DEFAULT"] = to_container()
        for key, val in iteritems(defaults):
            cnf["DEFAULT"][key] = _parse_val(val, sep)

    for sect in parser.sections():
        cnf[sect] = to_container()
        for key, val in parser.items(sect):
            cnf[sect][key] = _parse_val(val, sep)

    return cnf


def _dumps_itr(cnf):
    """
    :param cnf: Configuration data to dump
    """
    dkey = "DEFAULT"
    for sect, params in iteritems(cnf):
        yield "[%s]" % sect

        for key, val in iteritems(params):
            if sect != dkey and dkey in cnf and cnf[dkey].get(key) == val:
                continue  # It should be in [DEFAULT] section.

            yield "%s = %s" % (key, _to_s(val))

        yield ''  # it will be a separator between each sections.


def _dumps(cnf, **kwargs):
    """
    :param cnf: Configuration data to dump
    :param kwargs: optional keyword parameters to be sanitized :: dict

    :return: String representation of `cnf` object in INI format
    """
    return '\n'.join(l for l in _dumps_itr(cnf))


class Parser(anyconfig.backend.base.FromStreamLoader,
             anyconfig.backend.base.ToStringDumper):
    """
    Ini config files parser.
    """
    _type = "ini"
    _extensions = ["ini"]
    _load_opts = ["defaults", "dict_type", "allow_no_value", "filename",
                  "ac_parse_value"]

    dump_to_string = anyconfig.backend.base.to_method(_dumps)

    def load_from_stream(self, stream, to_container, **options):
        """
        Load config from given file like object `stream`.

        :param stream:  Config file or file like object
        :param to_container: callble to make a container object
        :param options: optional keyword arguments

        :return: Dict-like object holding config parameters
        """
        return _load(stream, to_container=to_container, **options)

# vim:sw=4:ts=4:et:
