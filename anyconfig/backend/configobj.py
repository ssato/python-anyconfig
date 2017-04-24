#
# Copyright (C) 2013 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
r"""Configobj backend:

- Format to support: configobj, http://goo.gl/JbP2Kp (readthedocs.org)
- Requirements: configobj (https://pypi.python.org/pypi/configobj/)
- Development Status :: 4 - Beta
- Limitations: AFAIK, configobj does not keep the order of configuration items
  and not have options to change this behavior like configparser, so this
  backend does not keep the order of configuration items even if the ac_ordered
  option was used.

- Special options:

  - All options except for 'infile' passed to configobj.ConfigObj.__init__
    should work.

  - See also: http://configobj.readthedocs.io/en/latest/configobj.html

Chnagelog:

.. versionchanged:: 0.5.0

   - Now loading and dumping options are detected automatically from inspection
     result if possible. Also these became not distinguished because these will
     be passed to configobj.Configuration anyway.
"""
from __future__ import absolute_import

import os
import configobj
import anyconfig.backend.base

from anyconfig.compat import getargspec


try:
    _LOAD_OPTS = [a for a in getargspec(configobj.ConfigObj).args
                  if a not in "self infile".split()]
except (TypeError, AttributeError):
    _LOAD_OPTS = ("options configspec encoding interpolation raise_errors"
                  "list_values create_empty file_error stringify"
                  "indent_type default_encoding unrepr write_empty_values"
                  "_inspec").split()


def make_configobj(cnf, **kwargs):
    """
    Make a configobj.ConfigObj initalized with given config `cnf`.

    :param cnf: Configuration data
    :param kwargs: optional keyword parameters passed to ConfigObj.__init__

    :return: An initialized configobj.ConfigObj instance
    """
    cobj = configobj.ConfigObj(**kwargs)
    cobj.update(cnf)

    return cobj


def load(path_or_strm, container, **opts):
    """
    :param path_or_strm: input config file path or file/file-like object
    :param container: callble to make a container object
    :param opts: keyword options passed to :class:`configobj.ConfigObj`

    :return: Mapping object
    """
    return container(configobj.ConfigObj(path_or_strm, **opts))


class Parser(anyconfig.backend.base.StreamParser,
             anyconfig.backend.base.BinaryFilesMixin):
    """
    Parser for Ini-like config files which configobj supports.
    """
    _type = "configobj"
    _priority = 10
    _load_opts = _LOAD_OPTS  # options on dump will be just ignored.
    _dump_opts = _LOAD_OPTS  # Likewise.
    _ordered = True

    load_from_path = load_from_stream = anyconfig.backend.base.to_method(load)

    def dump_to_string(self, cnf, **kwargs):
        """
        Dump config `cnf` to a string.

        :param cnf: Configuration data to dump
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: string represents the configuration
        """
        return os.linesep.join(make_configobj(cnf, **kwargs).write())

    def dump_to_stream(self, cnf, stream, **kwargs):
        """
        :param cnf: Configuration data to dump
        :param stream: Config file or file-like object
        :param kwargs: backend-specific optional keyword parameters :: dict
        """
        make_configobj(cnf, **kwargs).write(stream)

# vim:sw=4:ts=4:et:
