#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.base as Base

import logging
import sys


SUPPORTED = False
try:
    import pyjavaproperties
    SUPPORTED = True
except ImportError:
    sys.stderr.write(
        "pyjavaproperties module is not available. Disabled its support.\n"
    )

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


if SUPPORTED:
    def load_impl(config_fp, container):
        p = pyjavaproperties.Properties()
        p.load(config_fp)

        return container(p.getPropertyDict())

    def dump_impl(data, config_fp):
        """TODO: How to encode nested dicts?
        """
        p = pyjavaproperties.Properties()
        for k, v in data.iteritems():
            p.setProperty(k, v)

        p.store(config_fp)

else:
    def load_impl(config_fp, container):
        return container()

    def dump_impl(data, config_fp):
        pass


class PropertiesParser(Base.ConfigParser):

    _type = "properties"
    _extensions = ["properties"]

    #@classmethod
    #def loads(cls, config_content, *args, **kwargs):
    #    config_fp = StringIO.StringIO(config_content)
    #    return load_impl(config_fp, cls.container())

    @classmethod
    def load(cls, config_path, *args, **kwargs):
        return load_impl(open(config_path), cls.container())

    @classmethod
    def dumps(cls, data, *args, **kwargs):
        config_fp = StringIO.StringIO()
        dump_impl(data, config_fp)
        return config_fp.getvalue()

    @classmethod
    def dump(cls, data, config_path, *args, **kwargs):
        """TODO: How to encode nested dicts?
        """
        dump_impl(data, open(config_path, 'w'))


# vim:sw=4:ts=4:et:
