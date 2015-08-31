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


class Parser(anyconfig.backend.base.Parser):
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

    def load_impl(self, config_fp, **kwargs):
        """
        :param config_fp:  Config file object
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: dict object holding config parameters
        """
        return configobj.ConfigObj(config_fp, **kwargs)

    def dumps_impl(self, data, **kwargs):
        """
        :param data: Data to dump :: dict
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: string represents the configuration
        """
        conf = configobj.ConfigObj(**kwargs)
        conf.update(data)
        conf.filename = None

        return '\n'.join(conf.write())

    def dump_impl(self, data, config_path, **kwargs):
        """
        :param data: Data to dump :: dict
        :param config_path: Dump destination file path
        :param kwargs: backend-specific optional keyword parameters :: dict
        """
        conf = configobj.ConfigObj(**kwargs)
        conf.update(data)

        conf.write(open(config_path, 'wb'))

# vim:sw=4:ts=4:et:
