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
import anyconfig.mergeabledict
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

    container = anyconfig.mergeabledict.MergeableDict
    to_container = container.create

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

    def load_from_string(self, content, **kwargs):
        """
        Load config from given string `content`.

        :param content: Config content string
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: self.container object holding config parameters
        """
        return self.container()

    def load_from_path(self, filepath, **kwargs):
        """
        Load config from given file path `filepath`.

        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: self.container object holding config parameters
        """
        return self.container()

    def load_from_stream(self, stream, **kwargs):
        """
        Load config from given file like object `stream`.

        :param stream:  Config file or file like object
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: self.container object holding config parameters
        """
        return self.container()

    def loads(self, content, **kwargs):
        """
        Load config from given string `content` after some checks.

        :param content:  Config file content
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: self.container object holding config parameters
        """
        if not content or content is None:
            return self.container()

        kwargs = mk_opt_args(self._load_opts, kwargs)
        return self.to_container(self.load_from_string(content, **kwargs))

    def load(self, path_or_stream, ignore_missing=False, **kwargs):
        """
        Load config from a file path or a file / file-like object
        `path_or_stream` after some checks.

        :param path_or_stream: Config file path or file{,-like} object
        :param ignore_missing:
            Ignore and just return None if given `path_or_stream` is not a file
            / file-like object (thus, it should be a file path) and does not
            exist in actual
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: self.container object holding config parameters
        """
        kwargs = mk_opt_args(self._load_opts, kwargs)

        if isinstance(path_or_stream, anyconfig.compat.STR_TYPES):
            if ignore_missing and not os.path.exists(path_or_stream):
                return self.container()

            cnf = self.load_from_path(path_or_stream, **kwargs)
        else:
            cnf = self.load_from_stream(path_or_stream, **kwargs)

        return self.to_container(cnf)

    def dump_to_string(self, cnf, **kwargs):
        """
        Dump config `cnf` to a string.

        :param cnf: Configuration data to dump :: self.container
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: string represents the configuration
        """
        pass  # Dummy impl. e.g. str(cnf) ?

    def dump_to_path(self, cnf, filepath, **kwargs):
        """
        Dump config `cnf` to a file `filepath`.

        :param cnf: Configuration data to dump :: self.container
        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        pass

    def dump_to_stream(self, cnf, stream, **kwargs):
        """
        Dump config `cnf` to a file-like object `stream`.

        TODO: How to process socket objects same as file objects ?

        :param cnf: Configuration data to dump :: self.container
        :param stream:  Config file or file like object
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        pass

    def dumps(self, cnf, **kwargs):
        """
        Dump config `cnf` to a string.

        :param cnf: Configuration data to dump :: self.container
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: string represents the configuration
        """
        kwargs = mk_opt_args(self._dump_opts, kwargs)
        cnf = self.container.convert_to(cnf)
        return self.dump_to_string(cnf, **kwargs)

    def dump(self, cnf, path_or_stream, **kwargs):
        """
        Dump config `cnf` to a filepath or file-like object
        `path_or_stream`.

        :param cnf: Configuration data to dump :: self.container
        :param path_or_stream: Config file path or file{,-like} object
        :param kwargs: optional keyword parameters to be sanitized :: dict
        :raises IOError, OSError, AttributeError: When dump failed.
        """
        kwargs = mk_opt_args(self._dump_opts, kwargs)
        cnf = self.container.convert_to(cnf)

        if isinstance(path_or_stream, anyconfig.compat.STR_TYPES):
            ensure_outdir_exists(path_or_stream)
            self.dump_to_path(cnf, path_or_stream, **kwargs)
        else:
            self.dump_to_stream(cnf, path_or_stream, **kwargs)


class LParser(Parser):
    """
    Abstract config parser provides a method to load configuration from string
    content to help implement parser of which backend lacks of such function.

    Parser classes inherit this class have to override the method
    :meth:`load_from_stream` at least.
    """
    def load_from_string(self, content, **kwargs):
        """
        Load config from given string `cnf_content`.

        :param content: Config content string
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: self.container object holding config parameters
        """
        return self.load_from_stream(anyconfig.compat.StringIO(content))


class L2Parser(Parser):
    """
    Abstract config parser provides a method to load configuration from a file
    or file-like object (stream) to help implement parser of which backend
    lacks of such function.

    Parser classes inherit this class have to override the method
    :meth:`load_from_stream` at least.
    """
    def load_from_path(self, filepath, **kwargs):
        """
        Load config from given file path `filepath`.

        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: self.container object holding config parameters
        """
        return self.load_from_stream(self.ropen(filepath), **kwargs)


class DParser(Parser):
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

        :param cnf: Configuration data to dump :: self.container
        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        with self.wopen(filepath) as out:
            out.write(self.dump_to_string(cnf, **kwargs))

    def dump_to_stream(self, cnf, stream, **kwargs):
        """
        Dump config `cnf` to a file-like object `stream`.

        TODO: How to process socket objects same as file objects ?

        :param cnf: Configuration data to dump :: self.container
        :param stream:  Config file or file like object
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        stream.write(self.dump_to_string(cnf, **kwargs))


class D2Parser(Parser):
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

        :param cnf: Configuration data to dump :: self.container
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: self.container object holding config parameters
        """
        stream = self.to_stream()
        self.dump_to_stream(cnf, stream, **kwargs)
        return stream.getvalue()

    def dump_to_path(self, cnf, filepath, **kwargs):
        """
        Dump config `cnf` to a file `filepath`.

        :param cnf: Configuration data to dump :: self.container
        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        with self.wopen(filepath) as out:
            self.dump_to_stream(cnf, out, **kwargs)

# vim:sw=4:ts=4:et:
