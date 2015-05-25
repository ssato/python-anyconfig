#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""Abstract implementation of backend modules.
"""
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
    def filter_kwargs(kwargs):
        """
        Filter keyword arguments
        """
        for k in keys:
            if k in kwargs:
                yield (k, kwargs[k])

    return dict((k, v) for k, v in filter_kwargs(kwargs))


def mk_dump_dir_if_not_exist(f):
    """
    Make dir to dump f if that dir does not exist.

    :param f: path of file to dump
    """
    dumpdir = os.path.dirname(f)

    if not os.path.exists(dumpdir):
        LOGGER.debug("Creating output dir as it's not found: %s", dumpdir)
        os.makedirs(dumpdir)


class ConfigParser(object):
    """
    Abstract class of config files parsers
    """

    _type = None
    _priority = 0   # 0 (lowest priority) .. 99  (highest priority)
    _extensions = []
    _container = anyconfig.mergeabledict.MergeableDict

    _load_opts = []
    _dump_opts = []

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
    def supports(cls, config_file=None):
        """
        :return: True if this parser can process given file or is supported.
        """
        if config_file is None:
            return True

        return anyconfig.utils.get_file_extension(config_file) \
            in cls._extensions

    @classmethod
    def container(cls):
        """
        :return: Container object used in this class
        """
        return cls._container

    @classmethod
    def set_container(cls, container):
        """
        Setter of container of this class
        """
        cls._container = container

    @classmethod
    def exists(cls, config_path):
        """
        :return: True if given file `config_path` exists
        """
        return os.path.exists(config_path)

    @classmethod
    def load_impl(cls, config_fp, **kwargs):
        """
        :param config_fp:  Config file object
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: dict object holding config parameters
        """
        raise NotImplementedError("Inherited class should implement this")

    @classmethod
    def loads(cls, config_content, **kwargs):
        """
        :param config_content:  Config file content
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: cls.container() object holding config parameters
        """
        config_fp = anyconfig.compat.StringIO(config_content)
        create = cls.container().create
        return create(cls.load_impl(config_fp,
                                    **mk_opt_args(cls._load_opts, kwargs)))

    @classmethod
    def load(cls, config_path, ignore_missing=False, **kwargs):
        """
        :param config_path:  Config file path
        :param ignore_missing: Ignore and just return None if given file
            (``config_path``) does not exist
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: cls.container() object holding config parameters
        """
        if ignore_missing and not cls.exists(config_path):
            return cls.container()()

        create = cls.container().create
        return create(cls.load_impl(open(config_path),
                                    **mk_opt_args(cls._load_opts, kwargs)))

    @classmethod
    def dumps_impl(cls, data, **kwargs):
        """
        :param data: Data to dump :: dict
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: string represents the configuration
        """
        raise NotImplementedError("Inherited class should implement this")

    @classmethod
    def dump_impl(cls, data, config_path, **kwargs):
        """
        :param data: Data to dump :: dict
        :param config_path: Dump destination file path
        :param kwargs: backend-specific optional keyword parameters :: dict
        """
        open(config_path, "w").write(cls.dumps_impl(data, **kwargs))

    @classmethod
    def dumps(cls, data, **kwargs):
        """
        :param data: Data to dump :: cls.container()
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: string represents the configuration
        """
        convert_to = cls.container().convert_to
        return cls.dumps_impl(convert_to(data),
                              **mk_opt_args(cls._dump_opts, kwargs))

    @classmethod
    def dump(cls, data, config_path, **kwargs):
        """
        :param data: Data to dump :: cls.container()
        :param config_path: Dump destination file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        convert_to = cls.container().convert_to
        mk_dump_dir_if_not_exist(config_path)
        cls.dump_impl(convert_to(data), config_path,
                      **mk_opt_args(cls._dump_opts, kwargs))

# vim:sw=4:ts=4:et:
