#
# Copyright (C) 2011, 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.base as Base
import logging

SUPPORTED = False
try:
    import yaml
    SUPPORTED = True
except ImportError:
    logging.warn("YAML module is not available. Disabled its support.")

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


if SUPPORTED:
    class YamlConfigParser(Base.ConfigParser):

        _type = "yaml"
        _extensions = ["yaml", "yml"]

        @classmethod
        def loads(cls, config_content, *args, **kwargs):
            config_fp = StringIO.StringIO(config_content)
            create = cls.container().create

            return create(yaml.load(config_fp))

        @classmethod
        def load(cls, config_path, *args, **kwargs):
            create = cls.container().create

            return create(yaml.load(open(config_path)))

        @classmethod
        def dumps(cls, data, *args, **kwargs):
            return yaml.dump(data, None)

        @classmethod
        def dump(cls, data, config_path, *args, **kwargs):
            yaml.dump(data, open(config_path, "w"))


# vim:sw=4:ts=4:et:
