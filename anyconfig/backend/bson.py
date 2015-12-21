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


def _load_opts(use_c=None):
    """
    Decide loading options by bson._use_c.

    - No keyword args are permitted for decode_all() if bson._use_c == True
    - bson._use_c looks missing in python 3 version.

    :param use_c: bson._use_c

    >>> _load_opts(True)
    []
    >>> _load_opts(False)
    ['as_class', 'tz_aware', 'uuid_subtype']

    # >>> _load_opts()
    # <result varies depends on environment...>
    """
    if use_c is None:
        use_c = getattr(bson, "_use_c", None)

    if use_c is None or use_c:
        return []

    return ["as_class", "tz_aware", "uuid_subtype"]


class Parser(anyconfig.backend.base.FromStringLoader,
             anyconfig.backend.base.ToStringDumper):
    """
    Loader/Dumper of BSON files.
    """
    _type = "bson"
    _extensions = ["bson", "bsn"]  # Temporary.
    _load_opts = _load_opts()
    _dump_opts = ["check_keys", "uuid_subtype"]
    _open_flags = ('rb', 'wb')

    dump_to_string = anyconfig.backend.base.to_method(bson.BSON.encode)

    def load_from_string(self, content, **kwargs):
        """
        Load BSON config from given string `content`.

        :param content: BSON config content in bytes data string
        :param kwargs: optional keyword parameters

        :return: Dict-like object holding config parameters
        """
        objs = bson.decode_all(content, **kwargs)
        if objs:
            return anyconfig.mergeabledict.create_from(objs[0])
        else:
            return None

# vim:sw=4:ts=4:et:
