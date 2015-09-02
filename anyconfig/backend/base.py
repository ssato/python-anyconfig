#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=unused-argument
"""Abstract implementation of backend modules.

Backend module must implement a parser class inherits :class:`Parser` of this
module and override some of its methods, :method:`load_impl` and
:method:`dumps_impl` at least.
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

    if not os.path.exists(outdir):
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

    def loads(self, cnf_content, **kwargs):
        """
        Load config from given string `cnf_content` after some checks.

        :param cnf_content:  Config file content
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: self.container object holding config parameters
        """
        if not cnf_content or cnf_content is None:
            return self.container()

        kwargs = mk_opt_args(self._load_opts, kwargs)
        return self.container(self.load_from_string(cnf_content, **kwargs))

    def load(self, cnf_path_or_stream, ignore_missing=False, **kwargs):
        """
        :param cnf_path_or_stream: Config file path or file{,-like} object
        :param ignore_missing:
            Ignore and just return None if given file `cnf_path` does not exist
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: self.container object holding config parameters
        """
        kwargs = mk_opt_args(self._load_opts, kwargs)

        if isinstance(cnf_path_or_stream, anyconfig.compat.STR_TYPES):
            if ignore_missing and not os.path.exists(cnf_path_or_stream):
                return self.container()

            cnf = self.load_from_path(cnf_path_or_stream, **kwargs)
        else:
            cnf = self.load_from_stream(cnf_path_or_stream, **kwargs)

        return self.container(cnf)

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

    def dump(self, cnf, cnf_path_or_stream, **kwargs):
        """
        Dump config `cnf` to a filepath or file-like object
        `cnf_path_or_stream`.

        :param cnf: Configuration data to dump :: self.container
        :param cnf_path_or_stream: Config file path or file{,-like} object
        :param kwargs: optional keyword parameters to be sanitized :: dict
        :raises IOError, OSError, AttributeError: When dump failed.
        """
        kwargs = mk_opt_args(self._dump_opts, kwargs)
        cnf = self.container.convert_to(cnf)

        if isinstance(cnf_path_or_stream, anyconfig.compat.STR_TYPES):
            ensure_outdir_exists(cnf_path_or_stream)
            self.dump_to_path(cnf, cnf_path_or_stream, **kwargs)
        else:
            self.dump_to_stream(cnf, cnf_path_or_stream, **kwargs)


class LParser(Parser):
    """
    Abstract config parser provides a method to load configuration from string
    content to help implement parser of which backend lacks of such function.
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
    """
    def load_from_path(self, filepath, **kwargs):
        """
        Load config from given file path `filepath`.

        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: self.container object holding config parameters
        """
        return self.load_from_stream(open(filepath, self._open_flags[0]),
                                     **kwargs)


class DParser(Parser):
    """
    Abstract config parser provides a method to dump configuration to a file or
    file-like object (stream) and a file of given path to help implement parser
    of which backend lacks of such functions.
    """
    def dump_to_path(self, cnf, filepath, **kwargs):
        """
        Dump config `cnf` to a file `filepath`.

        :param cnf: Configuration data to dump :: self.container
        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        with open(filepath, self._open_flags[1]) as out:
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
        with open(filepath, self._open_flags[1]) as out:
            self.dump_to_stream(cnf, out, **kwargs)

# vim:sw=4:ts=4:et:
