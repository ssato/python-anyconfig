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
    _supported = SUPPORTED

    _load_opts = ["Loader"]
    _dump_opts = ["stream", "Dumper"]

    @classmethod
    def load_impl(cls, config_fp, **kwargs):
        """
        :param config_fp:  Config file content
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: dict object holding config parameters
        """
        return yaml_load(config_fp, **kwargs)

    @classmethod
    def dumps_impl(cls, data, **kwargs):
        """
        :param data: Data to dump :: dict
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: string represents the configuration
        """
        return yaml_dump(data, **kwargs)

    @classmethod
    def dump_impl(cls, data, config_path, **kwargs):
        """
        :param data: Data to dump :: dict
        :param config_path: Dump destination file path
        :param kwargs: backend-specific optional keyword parameters :: dict
        """
        yaml_dump(data, open(config_path, 'w'), **kwargs)

# vim:sw=4:ts=4:et:
