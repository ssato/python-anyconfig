#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=unused-argument
"""Abstract implementation of backend modules.

.. versionchanged:: 0.2
   The methods :meth:`load_impl`, :meth:`dump_impl` are deprecated and replaced
   with :meth:`load_from_stream` and :meth:`load_from_path`,
   :meth:`dump_to_string` and :meth:`dump_to_path` respectively.

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
from __future__ import absolute_import

import functools
import logging
import os

import anyconfig.compat
import anyconfig.mdicts
import anyconfig.utils


LOGGER = logging.getLogger(__name__)


def mk_opt_args(keys, kwargs):
    """
    Make optional kwargs valid and optimized for each backend.

    :param keys: optional argument names
    :param kwargs: keyword arguements to process

    >>> mk_opt_args(("aaa", ), dict(aaa=1, bbb=2))
    {'aaa': 1}
    >>> mk_opt_args(("aaa", ), dict(bbb=2))
    {}
    """
    return dict((k, kwargs[k]) for k in keys if k in kwargs)


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


def to_container_fn(**options):
    """
    :param options:
        Keyword options will be passed to :fnc:`to_container` in
        :mod:`anyconfig.mdicts` to decide which merge-able dict to
        wrap configurations.
    """
    return functools.partial(anyconfig.mdicts.to_container, **options)


class Parser(object):
    """
    Abstract parser to provide basic implementation of some methods, interfaces
    and members.
    """
    _type = None
    _priority = 0   # 0 (lowest priority) .. 99  (highest priority)
    _extensions = []
    _load_opts = []
    _dump_opts = []
    _open_flags = ('r', 'w')

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

    def _load_options(self, **kwargs):
        """
        Select backend specific loading options from `kwargs` only.
        """
        return mk_opt_args(self._load_opts, kwargs)

    def load_from_string(self, content, to_container, **kwargs):
        """
        Load config from given string `content`.

        :param content: Config content string
        :param to_container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        return to_container()

    def load_from_path(self, filepath, to_container, **kwargs):
        """
        Load config from given file path `filepath`.

        :param filepath: Config file path
        :param to_container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        return to_container()

    def load_from_stream(self, stream, to_container, **kwargs):
        """
        Load config from given file like object `stream`.

        :param stream:  Config file or file like object
        :param to_container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        return to_container()

    def loads(self, content, **options):
        """
        Load config from given string `content` after some checks.

        :param content:  Config file content
        :param options:
            options will be passed to backend specific loading functions.
            please note that options have to be sanitized w/ mk_opt_args later
            to filter out options not  in _load_opts.

        :return: dict or dict-like object holding configurations
        """
        to_container = to_container_fn(**options)
        if not content or content is None:
            return to_container()

        return self.load_from_string(content, to_container,
                                     **self._load_options(**options))

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
            please note that options have to be sanitized w/ mk_opt_args later
            to filter out options not  in _load_opts.

        :return: dict or dict-like object holding configurations
        """
        to_container = to_container_fn(**options)
        options = self._load_options(**options)

        if isinstance(path_or_stream, anyconfig.compat.STR_TYPES):
            if ignore_missing and not os.path.exists(path_or_stream):
                return to_container()

            cnf = self.load_from_path(path_or_stream, to_container, **options)
        else:
            cnf = self.load_from_stream(path_or_stream, to_container,
                                        **options)

        return cnf

    def dump_to_string(self, cnf, **kwargs):
        """
        Dump config `cnf` to a string.

        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: string represents the configuration
        """
        pass

    def dump_to_path(self, cnf, filepath, **kwargs):
        """
        Dump config `cnf` to a file `filepath`.

        :param cnf: Configuration data to dump
        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        pass

    def dump_to_stream(self, cnf, stream, **kwargs):
        """
        Dump config `cnf` to a file-like object `stream`.

        TODO: How to process socket objects same as file objects ?

        :param cnf: Configuration data to dump
        :param stream:  Config file or file like object
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        pass

    def dumps(self, cnf, **kwargs):
        """
        Dump config `cnf` to a string.

        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: string represents the configuration
        """
        cnf = anyconfig.mdicts.convert_to(cnf, **kwargs)
        kwargs = mk_opt_args(self._dump_opts, kwargs)
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
        cnf = anyconfig.mdicts.convert_to(cnf, **kwargs)
        kwargs = mk_opt_args(self._dump_opts, kwargs)

        if isinstance(path_or_stream, anyconfig.compat.STR_TYPES):
            ensure_outdir_exists(path_or_stream)
            self.dump_to_path(cnf, path_or_stream, **kwargs)
        else:
            self.dump_to_stream(cnf, path_or_stream, **kwargs)


class FromStringLoader(Parser):
    """
    Abstract config parser provides a method to load configuration from string
    content to help implement parser of which backend lacks of such function.

    Parser classes inherit this class have to override the method
    :meth:`load_from_string` at least.
    """
    def load_from_stream(self, stream, to_container, **kwargs):
        """
        Load config from given stream `stream`.

        :param stream: Config file or file-like object
        :param to_container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        return self.load_from_string(stream.read(), to_container, **kwargs)

    def load_from_path(self, filepath, to_container, **kwargs):
        """
        Load config from given file path `filepath`.

        :param filepath: Config file path
        :param to_container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        return self.load_from_stream(self.ropen(filepath), to_container,
                                     **kwargs)


class FromStreamLoader(Parser):
    """
    Abstract config parser provides a method to load configuration from string
    content to help implement parser of which backend lacks of such function.

    Parser classes inherit this class have to override the method
    :meth:`load_from_stream` at least.
    """
    def load_from_string(self, content, to_container, **kwargs):
        """
        Load config from given string `cnf_content`.

        :param content: Config content string
        :param to_container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        return self.load_from_stream(anyconfig.compat.StringIO(content),
                                     to_container, **kwargs)

    def load_from_path(self, filepath, to_container, **kwargs):
        """
        Load config from given file path `filepath`.

        :param filepath: Config file path
        :param to_container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        return self.load_from_stream(self.ropen(filepath), to_container,
                                     **kwargs)


class ToStringDumper(Parser):
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


class ToStreamDumper(Parser):
    """
    Abstract config parser provides methods to dump configuration to a string
    content or a file of given path to help implement parser of which backend
    lacks of such functions.

    Parser classes inherit this class have to override the method
    :meth:`dump_to_stream` at least.
    """
    to_stream = to_method(anyconfig.compat.StringIO)

    def dump_to_string(self, cnf, **kwargs):
        """
        Dump config `cnf` to a string.

        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        stream = self.to_stream()
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

# vim:sw=4:ts=4:et:
