#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Ref. python -c "import toml; help(toml); ..."
#
# pylint: disable=unused-argument
"""TOML backend.

.. versionadded:: 0.1.0

- Format to support: TOML, https://github.com/toml-lang/toml
- Requirements: (python) toml module, https://github.com/uiri/toml
- Limitations: None obvious
- Special options:

  - toml.{load{s,},dump{s,}} only accept '_dict' keyword option but it's not
    supported and will be ignored.
"""
from __future__ import absolute_import

import toml
import anyconfig.backend.base
from anyconfig.backend.base import to_method


class Parser(anyconfig.backend.base.FromStreamLoader2,
             anyconfig.backend.base.ToStreamDumper):
    """
    TOML parser.
    """
    _type = "toml"
    _extensions = ["toml"]

    load_from_string = to_method(toml.loads)
    load_from_stream = to_method(toml.load)
    dump_to_string = to_method(toml.dumps)
    dump_to_stream = to_method(toml.dump)

# vim:sw=4:ts=4:et:
