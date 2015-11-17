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

import anyconfig.backend.base
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


class Parser(anyconfig.backend.base.FromStreamLoader2,
             anyconfig.backend.base.ToStreamDumper):
    """
    Parser for JSON files.
    """
    _type = "json"
    _extensions = ["json", "jsn", "js"]
    _load_opts = _LOAD_OPTS
    _dump_opts = _DUMP_OPTS

    dump_to_string = anyconfig.backend.base.to_method(json.dumps)
    dump_to_stream = anyconfig.backend.base.to_method(json.dump)

    def load_from_string(self, content, **kwargs):
        """
        Load JSON config from given string `content`.

        :param content: JSON config content string
        :param kwargs: optional keyword parameters passed to json.loads

        :return: self.container object holding configuration
        """
        return json.loads(content, object_hook=self.container, **kwargs)

    def load_from_stream(self, stream, **kwargs):
        """
        Load JSON config from given file or file-like object `stream`.

        :param stream: JSON file or file-like object
        :param kwargs: optional keyword parameters passed to json.load

        :return: self.container object holding configuration
        """
        return json.load(stream, object_hook=self.container, **kwargs)

# vim:sw=4:ts=4:et:
