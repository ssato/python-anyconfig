#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.mergeabledict as D
import anyconfig.utils as U


SUPPORTED = False


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
        for k in keys:
            if k in kwargs:
                yield (k, kwargs[k])

    return dict((k, v) for k, v in filter_kwargs(kwargs))


class ConfigParser(object):

    _type = None
    _extensions = []
    _container = D.MergeableDict
    _supported = False

    @classmethod
    def type(cls):
        return cls._type

    @classmethod
    def supports(cls, config_file):
        return cls._supported and \
            U.get_file_extension(config_file) in cls._extensions

    @classmethod
    def container(cls):
        return cls._container

    @classmethod
    def set_container(cls, container):
        cls._container = container

    @classmethod
    def loads(cls, config_content, **kwargs):
        """
        :param config_content:  Config file content
        :return: cls.container object holding config parameters
        """
        raise NotImplementedError("Inherited class MUST implement this")

    @classmethod
    def load(cls, config_file, **kwargs):
        """
        :param config_file:  Config file path
        :return: cls.container object holding config parameters
        """
        raise NotImplementedError("Inherited class MUST implement this")

    @classmethod
    def dumps(cls, data, **kwargs):
        """
        :param data: Data to dump
        """
        return repr(data)  # or str(...) ?

    @classmethod
    def dump(cls, data, config_path, **kwargs):
        """
        :param data: Data to dump
        :param config_path: Dump destination file path
        """
        open(config_path, "w").write(cls.dumps(data))

# vim:sw=4:ts=4:et:
