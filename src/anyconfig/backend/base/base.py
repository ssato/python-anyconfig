#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
r"""Abstract implementation of backend modules:

Backend module must implement a parser class inherits :class:`Parser` or its
children classes of this module and override all or some of the methods as
needed:

  - :meth:`load_from_string`: Load config from string
  - :meth:`load_from_stream`: Load config from a file or file-like object
  - :meth:`load_from_path`: Load config from file of given path
  - :meth:`dump_to_string`: Dump config as a string
  - :meth:`dump_to_stream`: Dump config to a file or file-like object
  - :meth:`dump_to_path`: Dump config to a file of given path
"""
import io

import anyconfig.models.processor
import anyconfig.utils

from .loaders import (
    LoaderMixin, FromStringLoaderMixin, FromStreamLoaderMixin
)
from .mixins import TextFilesMixin
from .utils import (
    ensure_outdir_exists, not_implemented
)


class DumperMixin:
    """
    Mixin class to dump data.

    Inherited classes must implement the following methods.

    - :meth:`dump_to_string`: Dump config as a string
    - :meth:`dump_to_stream`: Dump config to a file or file-like object
    - :meth:`dump_to_path`: Dump config to a file of given path

    Member variables:

    - _dump_opts: Backend specific options on dump
    """
    _dump_opts = []

    def dump_to_string(self, cnf, **kwargs):
        """
        Dump config 'cnf' to a string.

        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: string represents the configuration
        """
        not_implemented(self, cnf, **kwargs)

    def dump_to_path(self, cnf, filepath, **kwargs):
        """
        Dump config 'cnf' to a file 'filepath'.

        :param cnf: Configuration data to dump
        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        not_implemented(self, cnf, filepath, **kwargs)

    def dump_to_stream(self, cnf, stream, **kwargs):
        """
        Dump config 'cnf' to a file-like object 'stream'.

        TODO: How to process socket objects same as file objects ?

        :param cnf: Configuration data to dump
        :param stream:  Config file or file like object
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        not_implemented(self, cnf, stream, **kwargs)

    def dumps(self, cnf, **kwargs):
        """
        Dump config 'cnf' to a string.

        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: string represents the configuration
        """
        kwargs = anyconfig.utils.filter_options(self._dump_opts, kwargs)
        return self.dump_to_string(cnf, **kwargs)

    def dump(self, cnf, ioi, **kwargs):
        """
        Dump config 'cnf' to output object of which 'ioi' refering.

        :param cnf: Configuration data to dump
        :param ioi:
            an 'anyconfig.globals.IOInfo' namedtuple object provides various
            info of input object to load data from

        :param kwargs: optional keyword parameters to be sanitized :: dict
        :raises IOError, OSError, AttributeError: When dump failed.
        """
        kwargs = anyconfig.utils.filter_options(self._dump_opts, kwargs)

        if anyconfig.utils.is_stream_ioinfo(ioi):
            self.dump_to_stream(cnf, ioi.src, **kwargs)
        else:
            ensure_outdir_exists(ioi.path)
            self.dump_to_path(cnf, ioi.path, **kwargs)


class Parser(TextFilesMixin, LoaderMixin, DumperMixin,
             anyconfig.models.processor.Processor):
    """
    Abstract parser to provide basic implementation of some methods, interfaces
    and members.

    - _type: Parser type indicate which format it supports
    - _priority: Priority to select it if there are other parsers of same type
    - _extensions: File extensions of formats it supports
    - _open_flags: Opening flags to read and write files

    .. seealso:: the doc of :class:`anyconfig.models.processor.Processor`
    """
    _cid = "base"


class ToStringDumperMixin(DumperMixin):
    """
    Abstract config parser provides a method to dump configuration to a file or
    file-like object (stream) and a file of given path to help implement parser
    of which backend lacks of such functions.

    Parser classes inherit this class have to override the method
    :meth:`dump_to_string` at least.
    """
    def dump_to_path(self, cnf, filepath, **kwargs):
        """
        Dump config 'cnf' to a file 'filepath'.

        :param cnf: Configuration data to dump
        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        with self.wopen(filepath) as out:
            out.write(self.dump_to_string(cnf, **kwargs))

    def dump_to_stream(self, cnf, stream, **kwargs):
        """
        Dump config 'cnf' to a file-like object 'stream'.

        TODO: How to process socket objects same as file objects ?

        :param cnf: Configuration data to dump
        :param stream:  Config file or file like object
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        stream.write(self.dump_to_string(cnf, **kwargs))


class ToStreamDumperMixin(DumperMixin):
    """
    Abstract config parser provides methods to dump configuration to a string
    content or a file of given path to help implement parser of which backend
    lacks of such functions.

    Parser classes inherit this class have to override the method
    :meth:`dump_to_stream` at least.
    """
    def dump_to_string(self, cnf, **kwargs):
        """
        Dump config 'cnf' to a string.

        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        stream = io.StringIO()
        self.dump_to_stream(cnf, stream, **kwargs)
        return stream.getvalue()

    def dump_to_path(self, cnf, filepath, **kwargs):
        """
        Dump config 'cnf' to a file 'filepath`.

        :param cnf: Configuration data to dump
        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        with self.wopen(filepath) as out:
            self.dump_to_stream(cnf, out, **kwargs)


class StringParser(Parser, FromStringLoaderMixin, ToStringDumperMixin):
    """
    Abstract parser based on :meth:`load_from_string` and
    :meth:`dump_to_string`.

    Parser classes inherit this class must define these methods.
    """


class StreamParser(Parser, FromStreamLoaderMixin, ToStreamDumperMixin):
    """
    Abstract parser based on :meth:`load_from_stream` and
    :meth:`dump_to_stream`.

    Parser classes inherit this class must define these methods.
    """


def load_with_fn(load_fn, content_or_strm, container, allow_primitives=False,
                 **options):
    """
    Load data from given string or stream 'content_or_strm'.

    :param load_fn: Callable to load data
    :param content_or_strm: data content or stream provides it
    :param container: callble to make a container object
    :param allow_primitives:
        True if the parser.load* may return objects of primitive data types
        other than mapping types such like JSON parser
    :param options: keyword options passed to 'load_fn'

    :return: container object holding data
    """
    ret = load_fn(content_or_strm, **options)
    if anyconfig.utils.is_dict_like(ret):
        return container() if (ret is None or not ret) else container(ret)

    return ret if allow_primitives else container(ret)


def dump_with_fn(dump_fn, data, stream, **options):
    """
    Dump 'data' to a string if 'stream' is None, or dump 'data' to a file or
    file-like object 'stream'.

    :param dump_fn: Callable to dump data
    :param data: Data to dump
    :param stream:  File or file like object or None
    :param options: optional keyword parameters

    :return: String represents data if stream is None or None
    """
    if stream is None:
        return dump_fn(data, **options)

    return dump_fn(data, stream, **options)


class StringStreamFnParser(Parser, FromStreamLoaderMixin, ToStreamDumperMixin):
    """
    Abstract parser utilizes load and dump functions each backend module
    provides such like json.load{,s} and json.dump{,s} in JSON backend.

    Parser classes inherit this class must define the followings.

    - _load_from_string_fn: Callable to load data from string
    - _load_from_stream_fn: Callable to load data from stream (file object)
    - _dump_to_string_fn: Callable to dump data to string
    - _dump_to_stream_fn: Callable to dump data to stream (file object)

    .. note::
       Callables have to be wrapped with :func:`to_method` to make 'self'
       passed to the methods created from them ignoring it.

    :seealso: :class:`anyconfig.backend.json.Parser`
    """
    _load_from_string_fn = None
    _load_from_stream_fn = None
    _dump_to_string_fn = None
    _dump_to_stream_fn = None

    def load_from_string(self, content, container, **options):
        """
        Load configuration data from given string 'content'.

        :param content: Configuration string
        :param container: callble to make a container object
        :param options: keyword options passed to '_load_from_string_fn'

        :return: container object holding the configuration data
        """
        return load_with_fn(self._load_from_string_fn, content, container,
                            allow_primitives=self.allow_primitives(),
                            **options)

    def load_from_stream(self, stream, container, **options):
        """
        Load data from given stream 'stream'.

        :param stream: Stream provides configuration data
        :param container: callble to make a container object
        :param options: keyword options passed to '_load_from_stream_fn'

        :return: container object holding the configuration data
        """
        return load_with_fn(self._load_from_stream_fn, stream, container,
                            allow_primitives=self.allow_primitives(),
                            **options)

    def dump_to_string(self, cnf, **kwargs):
        """
        Dump config 'cnf' to a string.

        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: string represents the configuration
        """
        return dump_with_fn(self._dump_to_string_fn, cnf, None, **kwargs)

    def dump_to_stream(self, cnf, stream, **kwargs):
        """
        Dump config 'cnf' to a file-like object 'stream'.

        TODO: How to process socket objects same as file objects ?

        :param cnf: Configuration data to dump
        :param stream:  Config file or file like object
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        dump_with_fn(self._dump_to_stream_fn, cnf, stream, **kwargs)

# vim:sw=4:ts=4:et:
