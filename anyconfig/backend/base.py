#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.utils as U


SUPPORTED = False


class BaseConfigParser(object):

    _type = None
    _extentions = []

    @classmethod
    def type(cls):
        return cls._type

    @classmethod
    def supports(cls, config_file):
        return U.get_file_extension(config_file) in cls._extentions

    @classmethod
    def load(cls, config_file, **kwargs):
        """
        @param config_file:  Config file path
        """
        raise NotImplementedError("Inherited class MUST implement this")

    @classmethod
    def dumps(cls, data, *args, **kwargs):
        """
        @param data: Data to dump
        """
        return repr(data)  # or str(...) ?

    @classmethod
    def dump(cls, data, config_path, *args, **kwargs):
        """
        @param data: Data to dump
        @param config_path: Dump destination file path
        """
        open(config_path, "w").write(cls.dumps(data))


# vim:sw=4:ts=4:et:
