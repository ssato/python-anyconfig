#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.base as Base
import anyconfig.Bunch as B

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


class PropertiesParser(Base.BaseConfigParser):

    _type = "properties"
    _extensions = ["properties"]

    @classmethod
    def load(cls, config_path, *args, **kwargs):
        p = pyjavaproperties.Properties()
        p.load(open(config_path))
        return B.Bunch(p.getPropertyDict())

    @classmethod
    def dump(cls, data, config_path, *args, **kwargs):
        """TODO: How to encode nested dicts?
        """
        p = pyjavaproperties.Properties()
        for k, v in data.iteritems():
            p.setProperty(k, v)

        p.store(open(config_path, 'w'))


# vim:sw=4:ts=4:et:
