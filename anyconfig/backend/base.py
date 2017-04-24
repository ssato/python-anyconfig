#
# Copyright (C) 2012 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=unused-argument
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

Changelog:

.. versionchanged:: 0.9.1

   - Rename the member _dict_options to `_dict_opts` to make consistent w/
     other members such as _load_opts.

.. versionchanged:: 0.8.3

   - Add `_ordered` membmer and a class method :meth:` ordered to
     :class:`Parser`.
   - Add `_dict_options` member to the class :class:`Parser`.

.. versionchanged:: 0.2

   - The methods :meth:`load_impl`, :meth:`dump_impl` are deprecated and
     replaced with :meth:`load_from_stream` and :meth:`load_from_path`,
     :meth:`dump_to_string` and :meth:`dump_to_path` respectively.
"""
from __future__ import absolute_import

import functools
import logging
import os

import anyconfig.compat
import anyconfig.utils


LOGGER = logging.getLogger(__name__)


def ensure_outdir_exists(filepath):
    """
    Make dir to dump `filepath` if that dir does not exist.

    :param filepath: path of file to dump
    """
    outdir = os.path.dirname(filepath)

    if outdir and not os.path.exists(outdir):
        LOGGER.debug("Making output dir: %s", outdir)
        os.makedirs(outdir)


def to_method(func):
    """
    Lift :func:`func` to a method; it will be called with the first argument
    `self` ignored.

    :param func: Any callable object
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function.
        """
        return func(*args[1:], **kwargs)

    return wrapper


def _not_implemented(*args, **kwargs):
    """
    Utility function to raise NotImplementedError.
    """
    raise NotImplementedError()


class TextFilesMixin(object):
    """Mixin class to open configuration files as a plain text.

    Arguments of :func:`open` is different depends on python versions.

    - python 2: https://docs.python.org/2/library/functions.html#open
    - python 3: https://docs.python.org/3/library/functions.html#open
    """
    _open_flags = ('r', 'w')

    @classmethod
    def ropen(cls, filepath, **kwargs):
        """
        :param filepath: Path to file to open to read data
        """
        return open(filepath, cls._open_flags[0], **kwargs)

    @classmethod
    def wopen(cls, filepath, **kwargs):
        """
        :param filepath: Path to file to open to write data to
        """
        return open(filepath, cls._open_flags[1], **kwargs)


class BinaryFilesMixin(TextFilesMixin):
    """Mixin class to open binary (byte string) configuration files.
    """
    _open_flags = ('rb', 'wb')


class LoaderMixin(object):
    """
    Mixin class to load data.

    Inherited classes must implement the following methods.

    - :meth:`load_from_string`: Load config from string
    - :meth:`load_from_stream`: Load config from a file or file-like object
    - :meth:`load_from_path`: Load config from file of given path

    Member variables:

    - _load_opts: Backend specific options on load
    - _ordered: True if the parser keep the order of items by default
    - _dict_opts: Backend options to customize dict class to make results
    """
    _load_opts = []
    _ordered = False
    _dict_opts = []

    @classmethod
    def ordered(cls):
        """
        :return: True if parser can keep the order of keys else False.
        """
        return cls._ordered

    @classmethod
    def dict_options(cls):
        """
        :return: List of dict factory options
        """
        return cls._dict_opts

    def _container_factory(self, **options):
        """
        The order of prirorities are ac_dict, backend specific dict class
        option, ac_ordered.

        :param options: Keyword options may contain 'ac_ordered'.
        :return: Factory (class or function) to make an container.
        """
        ac_dict = options.get("ac_dict", False)
        _dicts = [x for x in (options.get(o) for o in self.dict_options())
                  if x]

        if self.dict_options() and ac_dict and callable(ac_dict):
            return ac_dict  # Higher priority than ac_ordered.
        elif _dicts and callable(_dicts[0]):
            return _dicts[0]
        elif self.ordered() and options.get("ac_ordered", False):
            return anyconfig.compat.OrderedDict
        else:
            return dict

    def _load_options(self, container, **options):
        """
        Select backend specific loading options.
        """
        # Force set dict option if available in backend. For example,
        # options["object_hook"] will be OrderedDict if 'container' was
        # OrderedDict in JSON backend.
        for opt in self.dict_options():
            options.setdefault(opt, container)

        return anyconfig.utils.filter_options(self._load_opts, options)

    def load_from_string(self, content, container, **kwargs):
        """
        Load config from given string `content`.

        :param content: Config content string
        :param container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        _not_implemented(self, content, container, **kwargs)

    def load_from_path(self, filepath, container, **kwargs):
        """
        Load config from given file path `filepath`.

        :param filepath: Config file path
        :param container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        _not_implemented(self, filepath, container, **kwargs)

    def load_from_stream(self, stream, container, **kwargs):
        """
        Load config from given file like object `stream`.

        :param stream:  Config file or file like object
        :param container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        _not_implemented(self, stream, container, **kwargs)

    def loads(self, content, **options):
        """
        Load config from given string `content` after some checks.

        :param content:  Config file content
        :param options:
            options will be passed to backend specific loading functions.
            please note that options have to be sanitized w/
            :func:`~anyconfig.utils.filter_options` later to filter out options
            not in _load_opts.

        :return: dict or dict-like object holding configurations
        """
        container = self._container_factory(**options)
        if not content or content is None:
            return container()

        options = self._load_options(container, **options)
        return self.load_from_string(content, container, **options)

    def load(self, path_or_stream, ignore_missing=False, **options):
        """
        Load config from a file path or a file / file-like object
        `path_or_stream` after some checks.

        :param path_or_stream: Config file path or file{,-like} object
        :param ignore_missing:
            Ignore and just return None if given `path_or_stream` is not a file
            / file-like object (thus, it should be a file path) and does not
            exist in actual.
        :param options:
            options will be passed to backend specific loading functions.
            please note that options have to be sanitized w/
            :func:`~anyconfig.utils.filter_options` later to filter out options
            not in _load_opts.

        :return: dict or dict-like object holding configurations
        """
        container = self._container_factory(**options)
        options = self._load_options(container, **options)

        if isinstance(path_or_stream, anyconfig.compat.STR_TYPES):
            if ignore_missing and not os.path.exists(path_or_stream):
                return container()

            cnf = self.load_from_path(path_or_stream, container, **options)
        else:
            cnf = self.load_from_stream(path_or_stream, container, **options)

        return cnf


class DumperMixin(object):
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
        Dump config `cnf` to a string.

        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: string represents the configuration
        """
        _not_implemented(self, cnf, **kwargs)

    def dump_to_path(self, cnf, filepath, **kwargs):
        """
        Dump config `cnf` to a file `filepath`.

        :param cnf: Configuration data to dump
        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        _not_implemented(self, cnf, filepath, **kwargs)

    def dump_to_stream(self, cnf, stream, **kwargs):
        """
        Dump config `cnf` to a file-like object `stream`.

        TODO: How to process socket objects same as file objects ?

        :param cnf: Configuration data to dump
        :param stream:  Config file or file like object
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        _not_implemented(self, cnf, stream, **kwargs)

    def dumps(self, cnf, **kwargs):
        """
        Dump config `cnf` to a string.

        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: string represents the configuration
        """
        kwargs = anyconfig.utils.filter_options(self._dump_opts, kwargs)
        return self.dump_to_string(cnf, **kwargs)

    def dump(self, cnf, path_or_stream, **kwargs):
        """
        Dump config `cnf` to a filepath or file-like object
        `path_or_stream`.

        :param cnf: Configuration data to dump
        :param path_or_stream: Config file path or file{,-like} object
        :param kwargs: optional keyword parameters to be sanitized :: dict
        :raises IOError, OSError, AttributeError: When dump failed.
        """
        kwargs = anyconfig.utils.filter_options(self._dump_opts, kwargs)

        if isinstance(path_or_stream, anyconfig.compat.STR_TYPES):
            ensure_outdir_exists(path_or_stream)
            self.dump_to_path(cnf, path_or_stream, **kwargs)
        else:
            self.dump_to_stream(cnf, path_or_stream, **kwargs)


class Parser(TextFilesMixin, LoaderMixin, DumperMixin):
    """
    Abstract parser to provide basic implementation of some methods, interfaces
    and members.

    - _type: Parser type indicate which format it supports
    - _priority: Priority to select it if there are other parsers of same type
    - _extensions: File extensions of formats it supports
    - _open_flags: Opening flags to read and write files
    """
    _type = None
    _priority = 0   # 0 (lowest priority) .. 99  (highest priority)
    _extensions = []

    @classmethod
    def type(cls):
        """
        Parser's type
        """
        return cls._type

    @classmethod
    def priority(cls):
        """
        Parser's priority
        """
        return cls._priority

    @classmethod
    def extensions(cls):
        """
        File extensions which this parser can process
        """
        return cls._extensions


class FromStringLoaderMixin(LoaderMixin):
    """
    Abstract config parser provides a method to load configuration from string
    content to help implement parser of which backend lacks of such function.

    Parser classes inherit this class have to override the method
    :meth:`load_from_string` at least.
    """
    def load_from_stream(self, stream, container, **kwargs):
        """
        Load config from given stream `stream`.

        :param stream: Config file or file-like object
        :param container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        return self.load_from_string(stream.read(), container, **kwargs)

    def load_from_path(self, filepath, container, **kwargs):
        """
        Load config from given file path `filepath`.

        :param filepath: Config file path
        :param container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        return self.load_from_stream(self.ropen(filepath), container, **kwargs)


class FromStreamLoaderMixin(LoaderMixin):
    """
    Abstract config parser provides a method to load configuration from string
    content to help implement parser of which backend lacks of such function.

    Parser classes inherit this class have to override the method
    :meth:`load_from_stream` at least.
    """
    def load_from_string(self, content, container, **kwargs):
        """
        Load config from given string `cnf_content`.

        :param content: Config content string
        :param container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        return self.load_from_stream(anyconfig.compat.StringIO(content),
                                     container, **kwargs)

    def load_from_path(self, filepath, container, **kwargs):
        """
        Load config from given file path `filepath`.

        :param filepath: Config file path
        :param container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        return self.load_from_stream(self.ropen(filepath), container, **kwargs)


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
        Dump config `cnf` to a file `filepath`.

        :param cnf: Configuration data to dump
        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        with self.wopen(filepath) as out:
            out.write(self.dump_to_string(cnf, **kwargs))

    def dump_to_stream(self, cnf, stream, **kwargs):
        """
        Dump config `cnf` to a file-like object `stream`.

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
        Dump config `cnf` to a string.

        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        stream = anyconfig.compat.StringIO()
        self.dump_to_stream(cnf, stream, **kwargs)
        return stream.getvalue()

    def dump_to_path(self, cnf, filepath, **kwargs):
        """
        Dump config `cnf` to a file `filepath`.

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
    pass


class StreamParser(Parser, FromStreamLoaderMixin, ToStreamDumperMixin):
    """
    Abstract parser based on :meth:`load_from_stream` and
    :meth:`dump_to_stream`.

    Parser classes inherit this class must define these methods.
    """
    pass


def load_with_fn(load_fn, content_or_strm, container, **options):
    """
    Load data from given string or stream `content_or_strm`.

    :param load_fn: Callable to load data
    :param content_or_strm: data content or stream provides it
    :param container: callble to make a container object
    :param options: keyword options passed to `load_fn`

    :return: container object holding data
    """
    ret = load_fn(content_or_strm, **options)
    return container() if ret is None else container(ret)


def dump_with_fn(dump_fn, data, stream, **options):
    """
    Dump `data` to a string if `stream` is None, or dump `data` to a file or
    file-like object `stream`.

    :param dump_fn: Callable to dump data
    :param data: Data to dump
    :param stream:  File or file like object or None
    :param options: optional keyword parameters

    :return: String represents data if stream is None or None
    """
    if stream is None:
        return dump_fn(data, **options)

    dump_fn(data, stream, **options)


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
       Callables have to be wrapped with :func:`to_method` to make `self`
       passed to the methods created from them ignoring it.

    :seealso: :class:`anyconfig.backend.json.Parser`
    """
    _load_from_string_fn = None
    _load_from_stream_fn = None
    _dump_to_string_fn = None
    _dump_to_stream_fn = None

    def load_from_string(self, content, container, **options):
        """
        Load configuration data from given string `content`.

        :param content: Configuration string
        :param container: callble to make a container object
        :param options: keyword options passed to `_load_from_string_fn`

        :return: container object holding the configuration data
        """
        return load_with_fn(self._load_from_string_fn, content, container,
                            **options)

    def load_from_stream(self, stream, container, **options):
        """
        Load data from given stream `stream`.

        :param stream: Stream provides configuration data
        :param container: callble to make a container object
        :param options: keyword options passed to `_load_from_stream_fn`

        :return: container object holding the configuration data
        """
        return load_with_fn(self._load_from_stream_fn, stream, container,
                            **options)

    def dump_to_string(self, data, **options):
        """
        Dump `data` to a string.

        :param data: Data to dump
        :param options: optional keyword parameters

        :return: String represents given data
        """
        return dump_with_fn(self._dump_to_string_fn, data, None, **options)

    def dump_to_stream(self, data, stream, **options):
        """
        Dump `data` to a file or file-like object `stream`.

        :param data: Data to dump
        :param stream:  File or file like object
        :param options: optional keyword parameters
        """
        dump_with_fn(self._dump_to_stream_fn, data, stream, **options)

# vim:sw=4:ts=4:et:
