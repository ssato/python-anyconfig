#
# Copyright (C) 2015 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Ref. python -c "import bson; help(bson)"
#
r"""BSON backend:

- Format to support: BSON, http://bsonspec.org
- Requirements: bson in pymongo, https://pypi.python.org/pypi/pymongo/
- Development Status: 3 - Alpha
- Limitations: It seems that the APIs of bson.decode\* were changed a lot in
  the current version (3.3) of python-bson in pymongo and this backend might
  not work with it. I don't have a time to test with that latest version yet
  and it's only tested with the older one, 3.3.1.
- Special options:

  - All keyword options for :meth:`encode` (dump{s,}) and :meth:`decode`
    (load{s,}) of :class:`bson.BSON` except for as_class should just work.

  - See also: https://api.mongodb.org/python/current/api/bson/

Changelog:

.. versionchanged:: 0.8.3

   - follow changes of options of bson.BSON.{encode,decode} in its upstream and
     changed or added some keyword options including ones for bson.CodecOptions

.. versionchanged:: 0.5.0

   - utilize as_class keyword argument to allow container objects made directly
     on load if C extension is not used and enabled.

   - _load_opts() was removed because C extension looks forced to be enalbed if
     bson.has_c() == True, that is, C extension was built, installed and used.
     see also: https://jira.mongodb.org/browse/PYTHON-379

    .. versionadded:: 0.1.0
"""
from __future__ import absolute_import

import bson
import anyconfig.backend.base
import anyconfig.utils


_CO_OPTIONS = ("document_class", "tz_aware", "uuid_representation",
               "unicode_decode_error_handler", "tzinfo")


def _codec_options(**options):
    """
    bson.BSON.{decode{,_all},encode} can receive bson.CodecOptions.

    :return: :class:`~bson.CodecOptions`
    """
    opts = anyconfig.utils.filter_options(_CO_OPTIONS, options)
    return bson.CodecOptions(**opts)


class Parser(anyconfig.backend.base.StringParser,
             anyconfig.backend.base.BinaryFilesMixin):
    """
    Loader/Dumper of BSON files.
    """
    _type = "bson"
    _extensions = ["bson", "bsn"]  # Temporary.
    _load_opts = [] if bson.has_c() else ["codec_options"]
    _dump_opts = [] if bson.has_c() else ["check_keys", "codec_options"]
    _ordered = not bson.has_c()
    _dict_opts = [] if bson.has_c() else ["document_class"]

    def _load_options(self, container, **options):
        """
        :param container: callble to make a container object later
        """
        if "codec_options" not in options:
            options.setdefault("document_class", container)
            if any(k in options for k in _CO_OPTIONS):
                options["codec_options"] = _codec_options(**options)

        return anyconfig.utils.filter_options(self._load_opts, options)

    def load_from_string(self, content, container, **kwargs):
        """
        Load BSON config from given string `content`.

        :param content: BSON config content in bytes data string
        :param container: callble to make a container object
        :param kwargs: optional keyword parameters

        :return: Dict-like object holding config parameters
        """
        if self._load_opts:  # indicates that C extension is not used.
            objs = bson.decode_all(content, **kwargs)
        else:
            # .. note::
            #    The order of loaded configuration keys may be lost but
            #    there is no way to avoid that, AFAIK.
            objs = [container(x) for x in bson.decode_all(content)
                    if x is not None]

        return objs[0] if objs else None

    def dump_to_string(self, data, **options):
        """Dump BSON data `data` to a string.

        :param data: BSON Data to dump
        :param options: optional keyword parameters to be sanitized
        :return: string represents the configuration
        """
        if self._dump_opts:
            container = self._container_factory(**options)
            opts = self._load_options(container, **options)
            for key in self._dump_opts:
                if options.get(key, False):
                    opts[key] = options[key]
            return bson.BSON.encode(data, *opts)
        else:
            return bson.BSON.encode(data)

# vim:sw=4:ts=4:et:
