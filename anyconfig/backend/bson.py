#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Ref. python -c "import bson; help(bson)"
#
# Access to bson._use_c is required to switch loading options:
# pylint: disable=protected-access
"""BSON backend.

.. versionadded:: 0.1.0

- Format to support: BSON, http://bsonspec.org
- Requirements: bson in pymongo, https://pypi.python.org/pypi/pymongo/
- Limitations: None obvious
- Special options:

  - All keyword options for :meth:`encode` (dump{s,}) and :meth:`decode`
    (load{s,}) of :class:`bson.BSON` should just work.

  - See also: https://api.mongodb.org/python/current/api/bson/
"""
from __future__ import absolute_import

import bson
import anyconfig.backend.base


try:
    if bson._use_c:
        _LOAD_OPTS = []  # No keyword args are permitted for decode_all().
    else:
        _LOAD_OPTS = ["as_class", "tz_aware", "uuid_subtype"]
except AttributeError:  # _use_c looks missing in python 3 version.
    _LOAD_OPTS = []  # Keep it empty until making sure valid options.


class Parser(anyconfig.backend.base.FromStreamLoader2,
             anyconfig.backend.base.ToStringDumper):
    """
    Loader/Dumper of BSON files.
    """
    _type = "bson"
    _extensions = ["bson", "bsn"]  # Temporary.
    _load_opts = _LOAD_OPTS
    _dump_opts = ["check_keys", "uuid_subtype"]
    _open_flags = ('rb', 'wb')

    dump_to_string = anyconfig.backend.base.to_method(bson.BSON.encode)

    def load_from_string(self, content, **kwargs):
        """
        Load BSON config from given string `content`.

        :param content: BSON config content in bytes data string
        :param kwargs: optional keyword parameters

        :return: self.container() object holding config parameters
        """
        objs = bson.decode_all(content, **kwargs)
        return None if not objs else self.container.create(objs[0])

    def load_from_stream(self, stream, **kwargs):
        """
        Load BSON config from given file or file-like object `stream`.

        :param stream: Config file or file-like object
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: self.container() object holding config parameters
        """
        return self.load_from_string(stream.read(), **kwargs)

# vim:sw=4:ts=4:et:
