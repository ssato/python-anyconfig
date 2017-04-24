#
# Copyright (C) 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=too-many-ancestors
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


class Parser(anyconfig.backend.base.StringStreamFnParser,
             anyconfig.backend.base.BinaryFilesMixin):
    """Parser for CBOR files.
    """
    _type = "cbor"
    _extensions = ["cbor"]
    _dump_opts = ["sort_keys"]

    _load_from_string_fn = anyconfig.backend.base.to_method(cbor.loads)
    _load_from_stream_fn = anyconfig.backend.base.to_method(cbor.load)
    _dump_to_string_fn = anyconfig.backend.base.to_method(cbor.dumps)
    _dump_to_stream_fn = anyconfig.backend.base.to_method(cbor.dump)

# vim:sw=4:ts=4:et:
