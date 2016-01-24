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


_LOAD_OPTS = ["cls", "parse_float", "parse_int", "parse_constant"]
_DUMP_OPTS = ["skipkeys", "ensure_ascii", "check_circular", "allow_nan",
              "cls", "indent", "separators", "default", "sort_keys"]

# It seems that 'encoding' argument is not allowed in json.load[s] and
# json.dump[s] in JSON module in python 3.x.
if not anyconfig.compat.IS_PYTHON_3:
    _LOAD_OPTS.append("encoding")
    _DUMP_OPTS.append("encoding")

if not anyconfig.compat.IS_PYTHON_2_6:
    _LOAD_OPTS.append("object_pairs_hook")


class Parser(anyconfig.backend.base.FromStreamLoader,
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

    def _load(self, load_fn, cntnt_or_strm, to_container, **opts):
        """
        Load JSON config from given string or stream `cntnt_or_strm`.

        :param cntnt_or_strm: JSON config content or stream will provide it
        :param to_container: callble to make a container object
        :param opts: keyword options passed to `json.load[s]`

        :return: Dict-like object holding configuration
        """
        if "object_pairs_hook" in self._load_opts:
            opts["object_pairs_hook"] = anyconfig.compat.OrderedDict
            return to_container(load_fn(cntnt_or_strm, **opts))
        else:
            return load_fn(cntnt_or_strm, object_hook=to_container, **opts)

    def load_from_string(self, content, to_container, **opts):
        """
        Load JSON config from given string `content`.

        :param content: JSON config content
        :param to_container: callble to make a container object
        :param opts: keyword options passed to `json.loads`

        :return: Dict-like object holding configuration
        """
        return self._load(json.loads, content, to_container, **opts)

    def load_from_stream(self, stream, to_container, **opts):
        """
        Load JSON config from given stream `stream`.

        :param stream: Stream will provide JSON config content string
        :param to_container: callble to make a container object
        :param opts: keyword options passed to `json.load`

        :return: Dict-like object holding configuration
        """
        return self._load(json.load, stream, to_container, **opts)

# vim:sw=4:ts=4:et:
