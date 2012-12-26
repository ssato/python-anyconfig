#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.utils as U
import anyconfig.Bunch as B


SUPPORTED = False


class ConfigParser(object):

    _type = None
    _extensions = []
    _container = B.Bunch

    @classmethod
    def type(cls):
        return cls._type

    @classmethod
    def supports(cls, config_file):
        return U.get_file_extension(config_file) in cls._extensions

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
    def dumps(cls, data, *args, **kwargs):
        """
        :param data: Data to dump
        """
        return repr(data)  # or str(...) ?

    @classmethod
    def dump(cls, data, config_path, *args, **kwargs):
        """
        :param data: Data to dump
        :param config_path: Dump destination file path
        """
        open(config_path, "w").write(cls.dumps(data))

# vim:sw=4:ts=4:et:
