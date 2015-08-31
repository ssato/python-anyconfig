#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Ref. python -c "import json; help(json)"
#
# pylint: disable=import-error
"""JSON file backend.

- Format to support: JSON, http://www.json.org
- Requirements: json in python standard library (>= python 2.6) or simplejson
- Limitations: None obvious
- Special options:

  - All options of json.load{s,} and json.dump{s,} except object_hook
    should work.

  - See also: https://docs.python.org/3/library/json.html or
    https://docs.python.org/2/library/json.html dependent on the python version
    to use.
"""
from __future__ import absolute_import

import anyconfig.backend.base as Base
import anyconfig.compat

try:
    import json
except ImportError:
    import simplejson as json


_LOAD_OPTS = ["cls", "parse_float", "parse_int", "parse_constant",
              "object_pairs_hook"]

_DUMP_OPTS = ["skipkeys", "ensure_ascii", "check_circular", "allow_nan",
              "cls", "indent", "separators", "default", "sort_keys"]

# It seems that 'encoding' argument is not allowed in json.load[s] and
# json.dump[s] in JSON module in python 3.x.
if not anyconfig.compat.IS_PYTHON_3:
    _LOAD_OPTS.append("encoding")
    _DUMP_OPTS.append("encoding")


class Parser(Base.Parser):
    """
    Parser for JSON files.
    """
    _type = "json"
    _extensions = ["json", "jsn", "js"]
    _load_opts = _LOAD_OPTS
    _dump_opts = _DUMP_OPTS

    _funcs = dict(loads=json.loads, load=json.load,
                  dumps=json.dumps, dump=json.dump)

    def dict_to_container(self, json_obj_dict):
        """Convert dict to container.

        :param json_obj_dict: A dict or dict-like JSON object
        :return: A Parser.container object
        """
        return self.container.create(json_obj_dict)

    def loads(self, cnf_content, **kwargs):
        """
        :param cnf_content:  Config file content
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: self.container object holding config parameters
        """
        func = self._funcs["loads"]
        return func(cnf_content, object_hook=self.dict_to_container,
                    **Base.mk_opt_args(self._load_opts, kwargs))

    def load_impl(self, cnf_fp, **kwargs):
        """
        :param cnf_fp:  Config file object
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: self.container object holding config parameters
        """
        func = self._funcs["load"]
        return func(cnf_fp, object_hook=self.dict_to_container, **kwargs)

    def dumps_impl(self, data, **kwargs):
        """
        :param data: Data to dump :: dict
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: string represents the configuration
        """
        return self._funcs["dumps"](data, **kwargs)

    def dump_impl(self, data, cnf_path, **kwargs):
        """
        :param data: Data to dump :: dict
        :param cnf_path: Dump destination file path
        :param kwargs: backend-specific optional keyword parameters :: dict
        """
        self._funcs["dump"](data, open(cnf_path, self._open_flags[1]),
                            **kwargs)

# vim:sw=4:ts=4:et:
