#
# Copyright (C) 2015 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Ref. python -c "import toml; help(toml); ..."
#
# pylint: disable=unused-argument
r"""TOML backend:

- Format to support: TOML, https://github.com/toml-lang/toml
- Requirements: (python) toml module, https://github.com/uiri/toml
- Development Status :: 4 - Beta
- Limitations: None obvious
- Special options:

  - toml.load{s,} only accept '_dict' keyword option but it's used already to
    pass callable to make a container object.

Changelog:

    .. versionadded:: 0.1.0
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
    _ordered = True

    dump_to_string = to_method(toml.dumps)
    dump_to_stream = to_method(toml.dump)

    def load_from_string(self, content, container, **opts):
        """
        Load TOML config from given string `content`.

        :param content: TOML config content
        :param container: callble to make a container object
        :param opts: keyword options passed to `toml.loads`

        :return: Dict-like object holding configuration
        """
        return toml.loads(content, _dict=container, **opts)

    def load_from_stream(self, stream, container, **opts):
        """
        Load TOML config from given stream `stream`.

        :param stream: Stream will provide config content string
        :param container: callble to make a container object
        :param opts: keyword options passed to `toml.load`

        :return: Dict-like object holding configuration
        """
        return toml.load(stream, _dict=container, **opts)

# vim:sw=4:ts=4:et:
