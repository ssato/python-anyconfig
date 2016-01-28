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

  - toml.load{s,} only accept '_dict' keyword option but it's used already to
    pass callable to make a container object.
"""
from __future__ import absolute_import

import toml
import anyconfig.backend.base
from anyconfig.backend.base import to_method


class Parser(anyconfig.backend.base.FromStreamLoader,
             anyconfig.backend.base.ToStreamDumper):
    """
    TOML parser.
    """
    _type = "toml"
    _extensions = ["toml"]

    dump_to_string = to_method(toml.dumps)
    dump_to_stream = to_method(toml.dump)

    def load_from_string(self, content, to_container, **opts):
        """
        Load TOML config from given string `content`.

        :param content: TOML config content
        :param to_container: callble to make a container object
        :param opts: keyword options passed to `toml.loads`

        :return: Dict-like object holding configuration
        """
        return toml.loads(content, _dict=to_container, **opts)

    def load_from_stream(self, stream, to_container, **opts):
        """
        Load TOML config from given stream `stream`.

        :param stream: Stream will provide config content string
        :param to_container: callble to make a container object
        :param opts: keyword options passed to `toml.load`

        :return: Dict-like object holding configuration
        """
        return toml.load(stream, _dict=to_container, **opts)

# vim:sw=4:ts=4:et:
