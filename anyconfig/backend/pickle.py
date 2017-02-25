#
# Copyright (C) 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""Pickle backend.

- Format to support: Pickle
- Requirements: It should be available always.

  - pickle/cPickle in python 2 standard library:
    https://docs.python.org/2/library/pickle.html

  - pickle in python 3 standard library:
    https://docs.python.org/3/library/pickle.html

- Development Status :: 4 - Beta
- Limitations: None obvious
- Special options: All options of pickle.{load{s,},dump{s,}} should work.
"""
from __future__ import absolute_import

try:
    import cPickle as pickle
except ImportError:
    import pickle

import anyconfig.backend.base
import anyconfig.compat


if anyconfig.compat.IS_PYTHON_3:
    LOAD_OPTS = ["fix_imports", "encoding", "errors"]
    DUMP_OPTS = ["protocol", "fix_imports"]
else:
    LOAD_OPTS = []
    DUMP_OPTS = ["protocol"]


class Parser(anyconfig.backend.base.FromStreamLoader,
             anyconfig.backend.base.ToStreamDumper):
    """
    Parser for Pickle files.
    """
    _type = "pickle"
    _extensions = ["pkl", "pickle"]
    _load_opts = LOAD_OPTS
    _dump_opts = DUMP_OPTS
    _open_flags = ('rb', 'wb')

    dump_to_string = anyconfig.backend.base.to_method(pickle.dumps)
    dump_to_stream = anyconfig.backend.base.to_method(pickle.dump)

    def _load(self, load_fn, content_or_strm, to_container, **opts):
        """
        Load Pickle config from given string or stream `content_or_strm`.

        :param content_or_strm: Pickled config content or stream provides it
        :param to_container: callble to make a container object
        :param opts: keyword options passed to `pickle.load[s]`

        :return: Dict-like object holding configuration
        """
        return to_container(load_fn(content_or_strm, **opts))

    def load_from_string(self, content, to_container, **opts):
        """
        Load Pickle config from given string `content`.

        :param content: Pickled config content
        :param to_container: callble to make a container object
        :param opts: keyword options passed to `pickle.loads`

        :return: Dict-like object holding configuration
        """
        return self._load(pickle.loads, content, to_container, **opts)

    def load_from_stream(self, stream, to_container, **opts):
        """
        Load Pickle config from given stream `stream`.

        :param stream: Stream will provide Pickled config content string
        :param to_container: callble to make a container object
        :param opts: keyword options passed to `pickle.load`

        :return: Dict-like object holding configuration
        """
        return self._load(pickle.load, stream, to_container, **opts)

# vim:sw=4:ts=4:et:
