#
# Copyright (C) 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
r"""CBOR backend:

- Format to support: CBOR, http://cbor.io, https://tools.ietf.org/html/rfc7049
- Requirements: cbor, https://pypi.python.org/pypi/cbor
- Development Status :: 4 - Beta
- Limitations: None obvious
- Special options:

  - All options of cbor.load{s,} and cbor.dump{s,} should work.
  - See also: https://github.com/brianolson/cbor_py/blob/master/cbor/cbor.py

Changelog:

    .. versionadded:: 0.8.3
"""
from __future__ import absolute_import

import cbor

import anyconfig.backend.base
import anyconfig.compat

from anyconfig.backend.pickle import load_with_fn


class Parser(anyconfig.backend.base.FromStreamLoader,
             anyconfig.backend.base.ToStreamDumper):
    """
    Parser for CBOR files.
    """
    _type = "cbor"
    _extensions = ["cbor"]
    _load_opts = []
    _dump_opts = ["sort_keys"]
    _open_flags = ('rb', 'wb')

    dump_to_string = anyconfig.backend.base.to_method(cbor.dumps)
    dump_to_stream = anyconfig.backend.base.to_method(cbor.dump)
    _load = anyconfig.backend.base.to_method(load_with_fn)

    def load_from_string(self, content, to_container, **opts):
        """
        Load CBOR config from given string `content`.

        :param content: CBOR config content
        :param to_container: callble to make a container object
        :param opts: keyword options passed to `cbor.loads`

        :return: Dict-like object holding configuration
        """
        return self._load(cbor.loads, content, to_container, **opts)

    def load_from_stream(self, stream, to_container, **opts):
        """
        Load CBOR config from given stream `stream`.

        :param stream: Stream will provide CBOR config content string
        :param to_container: callble to make a container object
        :param opts: keyword options passed to `cbor.load`

        :return: Dict-like object holding configuration
        """
        return self._load(cbor.load, stream, to_container, **opts)

# vim:sw=4:ts=4:et:
