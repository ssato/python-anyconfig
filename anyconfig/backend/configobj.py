#
# Copyright (C) 2013 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""configobj backend.

- Format to support: configobj, http://goo.gl/JbP2Kp (readthedocs.org)
- Requirements: configobj (https://pypi.python.org/pypi/configobj/)
- Limitations: None obvious
- Special options:

  - All options except for 'infile' passed to configobj.ConfigObj.__init__
    should work.

  - See also: http://goo.gl/LcVOzZ (readthedocs.org)
"""
from __future__ import absolute_import

import configobj
import anyconfig.backend.base


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


class Parser(anyconfig.backend.base.FromStreamLoader,
             anyconfig.backend.base.ToStreamDumper):
    """
    Parser for Ini-like config files which configobj supports.
    """
    _type = "configobj"
    _priority = 10
    _load_opts = ["cls", "configspec", "encoding", "interpolation",
                  "raise_errors", "list_values", "create_empty", "file_error",
                  "stringify", "indent_type", "default_encoding", "unrepr",
                  "_inspec", ]
    _dump_opts = ["cls", "encoding", "list_values", "indent_type",
                  "default_encoding", "unrepr", "write_empty_values", ]
    _open_flags = ('rb', 'wb')

    load_from_path = anyconfig.backend.base.to_method(configobj.ConfigObj)
    load_from_stream = anyconfig.backend.base.to_method(configobj.ConfigObj)

    def dump_to_string(self, cnf, **kwargs):
        """
        Dump config `cnf` to a string.

        :param cnf: Configuration data to dump
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: string represents the configuration
        """
        return '\n'.join(make_configobj(cnf, **kwargs).write())

    def dump_to_stream(self, cnf, stream, **kwargs):
        """
        :param cnf: Configuration data to dump
        :param stream: Config file or file-like object
        :param kwargs: backend-specific optional keyword parameters :: dict
        """
        make_configobj(cnf, **kwargs).write(stream)

# vim:sw=4:ts=4:et:
