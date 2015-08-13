#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""INI or INI like config files backend.

- Format to support: INI or INI like ones
- Requirements: It should be available always.

  - ConfigParser in python 2 standard library:
    https://docs.python.org/2.7/library/configparser.html

  - configparser in python 3 standard library:
    https://docs.python.org/3/library/configparser.html

- Limitations: None obvious
- Special options: None Obvious
"""
from __future__ import absolute_import

import logging
import sys

import anyconfig.backend.base as Base
import anyconfig.parser as P
import anyconfig.utils

from anyconfig.compat import configparser, iteritems


LOGGER = logging.getLogger(__name__)
_SEP = ','


# FIXME: May be too naive implementation.
def _parse(val_s, sep=_SEP):
    """
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


def _load_impl(config_fp, sep=_SEP, **kwargs):
    """
    :param config_fp: File or file-like object provides ini-style conf
    :return: Dict or dict-like object represents config values
    """
    config = dict()

    # Optional arguements for configparser.SafeConfigParser{,readfp}
    kwargs_0 = Base.mk_opt_args(("defaults", "dict_type", "allow_no_value"),
                                kwargs)
    kwargs_1 = Base.mk_opt_args(("filename", ), kwargs)

    try:
        try:
            parser = configparser.SafeConfigParser(**kwargs_0)
        except TypeError:
            # It seems ConfigPaser.*ConfigParser in python 2.6 does not support
            # 'allow_no_value' option parameter, and TypeError will be thrown.
            kwargs_0 = Base.mk_opt_args(("defaults", "dict_type"), kwargs)
            parser = configparser.SafeConfigParser(**kwargs_0)

        parser.readfp(config_fp, **kwargs_1)

        if parser.defaults():
            config["DEFAULT"] = dict()

            for key, val in iteritems(parser.defaults()):
                config["DEFAULT"][key] = _parse(val, sep)

        for sect in parser.sections():
            config[sect] = dict()

            for key, val in parser.items(sect):
                config[sect][key] = _parse(val, sep)

    except Exception:
        LOGGER.warn(sys.exc_info()[-1])
        raise

    return config


def mk_lines_g(data):
    """
    Make lines from given `data`
    """
    has_default = "DEFAULT" in data

    def is_inherited_from_default(key, val):
        """
        :return: True if (key, val) pair in defaults.
        """
        return has_default and data["DEFAULT"].get(key, None) == val

    for sect, params in iteritems(data):
        yield "[%s]\n" % sect

        for key, val in iteritems(params):
            if sect != "DEFAULT" and is_inherited_from_default(key, val):
                continue

            yield "%s = %s\n" % (key, _to_s(val))

        yield "\n"  # put an empty line just after each sections.


class Parser(Base.Parser):
    """
    Init config files parser.
    """
    _type = "ini"
    _extensions = ["ini"]
    _load_opts = ["defaults", "dict_type", "allow_no_value", "filename"]

    @classmethod
    def load_impl(cls, config_fp, **kwargs):
        """
        :param config_fp:  Config file object
        :param kwargs: configparser specific optional keyword parameters

        :return: dict object holding config parameters
        """
        return _load_impl(config_fp, sep=_SEP, **kwargs)

    @classmethod
    def dumps_impl(cls, data, **kwargs):
        """
        :param data: Data to dump :: dict
        :param config_path: Dump destination file path
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: string represents the configuration
        """
        return '\n'.join(l for l in mk_lines_g(data))

# vim:sw=4:ts=4:et:
