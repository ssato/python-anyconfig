#
# Copyright (C) 2011 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Ref. python -c "import json; help(json)"
#
# pylint: disable=import-error
r"""JSON backend:

- Format to support: JSON, http://www.json.org
- Requirements: json in python standard library (>= python 2.6) or simplejson
- Development Status :: 5 - Production/Stable
- Limitations: None obvious
- Special options:

  - All options of json.load{s,} and json.dump{s,} except object_hook
    should work.

  - See also: https://docs.python.org/3/library/json.html or
    https://docs.python.org/2/library/json.html dependent on the python version
    to use.

Changelog:

    .. versionadded:: 0.0.1
"""
from __future__ import absolute_import

try:
    import json
except ImportError:
    import simplejson as json

import anyconfig.backend.base
import anyconfig.compat


_LOAD_OPTS = ["cls", "object_hook", "parse_float", "parse_int",
              "parse_constant"]
_DUMP_OPTS = ["skipkeys", "ensure_ascii", "check_circular", "allow_nan",
              "cls", "indent", "separators", "default", "sort_keys"]
_DICT_OPTS = ["object_hook"]

# It seems that 'encoding' argument is not allowed in json.load[s] and
# json.dump[s] in JSON module in python 3.x.
if not anyconfig.compat.IS_PYTHON_3:
    _LOAD_OPTS.append("encoding")
    _DUMP_OPTS.append("encoding")

if not anyconfig.compat.IS_PYTHON_2_6:
    _LOAD_OPTS.append("object_pairs_hook")
    _DICT_OPTS.insert(0, "object_pairs_hook")  # Higher prio. than object_hook


class Parser(anyconfig.backend.base.StringStreamFnParser):
    """
    Parser for JSON files.
    """
    _type = "json"
    _extensions = ["json", "jsn", "js"]
    _load_opts = _LOAD_OPTS
    _dump_opts = _DUMP_OPTS
    _ordered = not anyconfig.compat.IS_PYTHON_2_6
    _dict_opts = _DICT_OPTS

    _load_from_string_fn = anyconfig.backend.base.to_method(json.loads)
    _load_from_stream_fn = anyconfig.backend.base.to_method(json.load)
    _dump_to_string_fn = anyconfig.backend.base.to_method(json.dumps)
    _dump_to_stream_fn = anyconfig.backend.base.to_method(json.dump)

# vim:sw=4:ts=4:et:
