#
# Copyright (C) 2015, 2016 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Ref. python -c "import bson; help(bson)"
#
# Access to bson._use_c is required to switch loading options:
# pylint: disable=protected-access
r"""BSON backend.

.. versionchanged:: 0.5.0

   - utilize as_class keyword argument to allow container objects made directly
     on load if C extension is not used and enabled.
   - _load_opts() was removed because C extension looks forced to be enalbed
     if bson.has_c() == True, that is, C extension was built. see also:
     https://jira.mongodb.org/browse/PYTHON-379

.. versionadded:: 0.1.0

- Format to support: BSON, http://bsonspec.org
- Requirements: bson in pymongo, https://pypi.python.org/pypi/pymongo/
- Limitations: It seems that the APIs of bson.decode\* were changed a lot in
  the current version (3.2) of python-bson in pymongo and this backend might
  not work with it. I don't have a time to test with that latest version yet
  and it's only tested with the older one, 2.5.2.
- Special options:

  - All keyword options for :meth:`encode` (dump{s,}) and :meth:`decode`
    (load{s,}) of :class:`bson.BSON` except for as_class should just work.

  - See also: https://api.mongodb.org/python/current/api/bson/
"""
from __future__ import absolute_import

import bson
import anyconfig.backend.base


class Parser(anyconfig.backend.base.FromStringLoader,
             anyconfig.backend.base.ToStringDumper):
    """
    Loader/Dumper of BSON files.
    """
    _type = "bson"
    _extensions = ["bson", "bsn"]  # Temporary.
    _load_opts = [] if bson.has_c() else ["tz_aware", "uuid_subtype"]
    _dump_opts = ["check_keys", "uuid_subtype"]
    _open_flags = ('rb', 'wb')

    dump_to_string = anyconfig.backend.base.to_method(bson.BSON.encode)

    def load_from_string(self, content, to_container, **kwargs):
        """
        Load BSON config from given string `content`.

        :param content: BSON config content in bytes data string
        :param to_container: callble to make a container object
        :param kwargs: optional keyword parameters

        :return: Dict-like object holding config parameters
        """
        if self._load_opts:  # indicates that C extension is not used.
            objs = bson.decode_all(content, as_class=to_container, **kwargs)
        else:
            # .. note::
            #    The order of loaded configuration keys may be lost but
            #    there is no way to avoid that, AFAIK.
            objs = to_container(bson.decode_all(content))

        return objs[0] if objs else None

# vim:sw=4:ts=4:et:
