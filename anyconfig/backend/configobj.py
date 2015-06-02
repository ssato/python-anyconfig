#
# Copyright (C) 2013 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""configobj backend for anyconfig.
"""
from __future__ import absolute_import

import configobj
import anyconfig.backend.base


class Parser(anyconfig.backend.base.Parser):
    """
    Parser for Ini-like config files which configobj supports.

    - Backend: configobj (https://pypi.python.org/pypi/configobj/)
    - Limitations: None obvious
    - Special options:

      - All options passed to configobj.ConfigObj.__init__ should work.
    """
    _type = "configobj"
    _priority = 10
    _load_opts = ["cls", "configspec", "encoding", "interpolation",
                  "raise_errors", "list_values", "create_empty", "file_error",
                  "stringify", "indent_type", "default_encoding", "unrepr",
                  "_inspec", ]
    _dump_opts = ["cls", "encoding", "list_values", "indent_type",
                  "default_encoding", "unrepr", "write_empty_values", ]

    @classmethod
    def load_impl(cls, config_fp, **kwargs):
        """
        :param config_fp:  Config file object
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: dict object holding config parameters
        """
        return configobj.ConfigObj(config_fp, **kwargs)

    @classmethod
    def dumps_impl(cls, data, **kwargs):
        """
        :param data: Data to dump :: dict
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: string represents the configuration
        """
        conf = configobj.ConfigObj(**kwargs)
        conf.update(data)
        conf.filename = None

        return '\n'.join(conf.write())

    @classmethod
    def dump_impl(cls, data, config_path, **kwargs):
        """
        :param data: Data to dump :: dict
        :param config_path: Dump destination file path
        :param kwargs: backend-specific optional keyword parameters :: dict
        """
        conf = configobj.ConfigObj(**kwargs)
        conf.update(data)

        conf.write(open(config_path, 'w'))

# vim:sw=4:ts=4:et:
