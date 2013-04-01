#
# Copyright (C) 2011 - 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
from anyconfig.compat import StringIO
from anyconfig.globals import LOGGER as logging

import anyconfig.backend.base as Base

SUPPORTED = False
try:
    import yaml
    SUPPORTED = True
except ImportError:
    logging.warn("YAML module is not available. Disabled its support.")


_LOAD_OPTS = ["Loader"]
_DUMP_TOPS = ["stream", "Dumper"]

if SUPPORTED:
    yaml_load = yaml.load
    yaml_dump = yaml.dump
else:
    def _dummy_fun(*args, **kwargs):
        logging.warn("Does nothing as YAML module is not available.")
        return

    yaml_load = yaml_dump = _dummy_fun


class YamlConfigParser(Base.ConfigParser):

    _type = "yaml"
    _extensions = ("yaml", "yml")

    @classmethod
    def loads(cls, config_content, **kwargs):
        config_fp = StringIO(config_content)
        create = cls.container().create

        return create(yaml_load(config_fp,
                                **Base.mk_opt_args(_LOAD_OPTS, kwargs)))

    @classmethod
    def load(cls, config_path, **kwargs):
        create = cls.container().create

        return create(yaml_load(open(config_path),
                                **Base.mk_opt_args(_LOAD_OPTS, kwargs)))

    @classmethod
    def dumps(cls, data, **kwargs):
        convert_to = cls.container().convert_to
        return yaml_dump(convert_to(data),
                         **Base.mk_opt_args(_DUMP_TOPS, kwargs))

    @classmethod
    def dump(cls, data, config_path, **kwargs):
        convert_to = cls.container().convert_to
        yaml_dump(convert_to(data), open(config_path, "w"),
                  **Base.mk_opt_args(_DUMP_TOPS, kwargs))

# vim:sw=4:ts=4:et:
