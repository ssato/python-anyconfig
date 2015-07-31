#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Ref. python -c "import msgpack; help(msgpack.Unpacker); help(msgpack.Packer)"
#
"""MessagePack file backend.
"""
from __future__ import absolute_import

import msgpack
import anyconfig.backend.json


_LOAD_OPTS = ["read_size", "use_list", "object_pairs_hook", "list_hook",
              "encoding", "unicode_errors", "max_buffer_size", "ext_hook",
              "max_str_len", "max_bin_len", "max_array_len", "max_map_len",
              "max_ext_len", "object_pairs_hook"]

_DUMP_OPTS = ["default", "encoding", "unicode_errors", "use_single_float",
              "autoreset", "use_bin_type"]


class Parser(anyconfig.backend.json.Parser):
    """
    Loader/Dumper for MessagePack files.

    - Backend: python-msgpack (msgpack)
    - Limitations: None obvious
    - Special options:

      - All options of msgpack.load{s,} and msgpack.dump{s,} except object_hook
        and file_like should work.
    """
    _type = "msgpack"
    _extensions = []
    _load_opts = _LOAD_OPTS
    _dump_opts = _DUMP_OPTS
    _funcs = dict(loads=msgpack.unpackb, load=msgpack.unpack,
                  dumps=msgpack.packb, dump=msgpack.pack)

    _open_flags = ('rb', 'wb')

# vim:sw=4:ts=4:et:
