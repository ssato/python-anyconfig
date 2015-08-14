#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Ref. python -c "import bson; help(bson)"
#
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


if bson._use_c:
    _LOAD_OPTS = []  # No keyword args are permitted for decode_all().
else:
    _LOAD_OPTS = ["as_class", "tz_aware", "uuid_subtype"]


class Parser(anyconfig.backend.base.Parser):
    """
    Loader/Dumper for MessagePack files.
    """
    _type = "bson"
    _extensions = [".bson", ".bsn"]  # Temporary.
    _load_opts = _LOAD_OPTS
    _dump_opts = ["check_keys", "uuid_subtype"]
    _open_flags = ('rb', 'wb')

    @classmethod
    def loads(cls, config_s, **kwargs):
        """
        :param config_s: Config content in bytes data string
        :param kwargs: optional keyword parameters

        :return: cls.container() object holding config parameters
        """
        kwargs = anyconfig.backend.base.mk_opt_args(cls._load_opts, kwargs)
        objs = bson.decode_all(config_s, **kwargs)
        return None if not objs else cls.container().create(objs[0])

    @classmethod
    def load_impl(cls, config_fp, **kwargs):
        """
        :param config_fp: Config file object
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: dict-like object holding config parameters
        """
        return cls.loads(config_fp.read(), **kwargs)

    @classmethod
    def dumps_impl(cls, obj, **kwargs):
        """
        :param obj: A dict or dict-like object to dump
        :param kwargs: Optional keyword parameters

        :return: string represents the configuration
        """
        return bson.BSON.encode(obj, **kwargs)

# vim:sw=4:ts=4:et:
