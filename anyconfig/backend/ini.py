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

import anyconfig.backend.base as Base
import anyconfig.parser as P
import anyconfig.utils

from anyconfig.compat import configparser, iteritems


_SEP = ','


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


def _load(filepath=None, stream=None, sep=_SEP, cls=dict, **kwargs):
    """
    :param filepath: Config file path
    :param stream: File or file-like object provides ini-style conf
    :param sep: Seprator string
    :param cls: Container class

    :return: Dict or dict-like object represents config values
    """
    if filepath is None and stream is None:
        raise ValueError("filepath or stream must be some value "
                         "other than None")
    cnf = cls()

    # Optional arguements for configparser.SafeConfigParser{,readfp}
    kwargs_0 = Base.mk_opt_args(("defaults", "dict_type", "allow_no_value"),
                                kwargs)
    kwargs_1 = Base.mk_opt_args(("filename", ), kwargs)

    try:
        parser = configparser.SafeConfigParser(**kwargs_0)
    except TypeError:
        # It seems ConfigPaser.*ConfigParser in python 2.6 does not support
        # 'allow_no_value' option parameter, and TypeError will be thrown.
        kwargs_0 = Base.mk_opt_args(("defaults", "dict_type"), kwargs)
        parser = configparser.SafeConfigParser(**kwargs_0)

    if filepath is None:
        parser.readfp(stream, **kwargs_1)
    else:
        parser.read(filepath, **kwargs_1)

    if parser.defaults():
        cnf["DEFAULT"] = cls()

        for key, val in iteritems(parser.defaults()):
            cnf["DEFAULT"][key] = _parse(val, sep)

    for sect in parser.sections():
        cnf[sect] = cls()

        for key, val in parser.items(sect):
            cnf[sect][key] = _parse(val, sep)

    return cnf


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


class Parser(Base.LParser):
    """
    Ini config files parser.
    """
    _type = "ini"
    _extensions = ["ini"]
    _load_opts = ["defaults", "dict_type", "allow_no_value", "filename"]

    def load_from_path(self, filepath, **kwargs):
        """
        Load config from given file path `filepath`.

        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: self.container object holding config parameters
        """
        return _load(filepath=filepath, sep=_SEP, cls=self.container, **kwargs)

    def load_from_stream(self, stream, **kwargs):
        """
        Load INI config from given file or file-like object `stream`.

        :param stream: Config file or file-like object
        :param kwargs: configparser specific optional keyword parameters

        :return: dict object holding config parameters
        """
        return _load(stream=stream, sep=_SEP, cls=self.container, **kwargs)

    def dump_to_string(self, cnf, **kwargs):
        """
        Dump INI config `cnf` to a string.

        :param cnf: Configuration data to dump :: self.container
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: string represents the configuration
        """
        return '\n'.join(l for l in mk_lines_g(cnf))

# vim:sw=4:ts=4:et:
