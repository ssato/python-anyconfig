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


class Parser(anyconfig.backend.base.Parser):
    """
    Loader/Dumper for MessagePack files.
    """
    _type = "bson"
    _extensions = [".bson", ".bsn"]  # Temporary.
    _load_opts = _LOAD_OPTS
    _dump_opts = ["check_keys", "uuid_subtype"]
    _open_flags = ('rb', 'wb')

    def loads(self, cnf_content, **kwargs):
        """
        :param cnf_content: Config content in bytes data string
        :param kwargs: optional keyword parameters

        :return: self.container() object holding config parameters
        """
        kwargs = anyconfig.backend.base.mk_opt_args(self._load_opts, kwargs)
        objs = bson.decode_all(cnf_content, **kwargs)
        return None if not objs else self.container.create(objs[0])

    def load_impl(self, cnf_fp, **kwargs):
        """
        :param cnf_fp: Config file object
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: dict-like object holding config parameters
        """
        return self.loads(cnf_fp.read(), **kwargs)

    def dumps_impl(self, obj, **kwargs):
        """
        :param obj: A dict or dict-like object to dump
        :param kwargs: Optional keyword parameters

        :return: string represents the configuration
        """
        return bson.BSON.encode(obj, **kwargs)

# vim:sw=4:ts=4:et:
