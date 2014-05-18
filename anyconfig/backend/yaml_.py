#
# Copyright (C) 2011 - 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
from anyconfig.globals import LOGGER as logging

import anyconfig.backend.base as Base

SUPPORTED = False
try:
    import yaml
    SUPPORTED = True
except ImportError:
    logging.warn("YAML module is not available. Disabled its support.")


if SUPPORTED:
    def filter_keys(keys, filter_key):
        return [k for k in keys if k != filter_key]

    def yaml_load(fp, **kwargs):
        keys = filter_keys(kwargs.keys(), "safe")
        if kwargs.get("safe", False):
            return yaml.safe_load(fp, **Base.mk_opt_args(keys, kwargs))
        else:
            return yaml.load(fp, **kwargs)

    def yaml_dump(data, fp, **kwargs):
        keys = filter_keys(kwargs.keys(), "safe")
        if kwargs.get("safe", False):
            return yaml.safe_dump(data, fp, **Base.mk_opt_args(keys, kwargs))
        else:
            return yaml.dump(data, fp, **kwargs)
else:
    def _dummy_fun(*args, **kwargs):
        logging.warn("Does nothing as YAML module is not available.")
        return

    yaml_load = yaml_dump = _dummy_fun


class YamlConfigParser(Base.ConfigParser):

    _type = "yaml"
    _extensions = ("yaml", "yml")
    _supported = SUPPORTED

    _load_opts = ["Loader", "safe"]
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
        return yaml_dump(data, None, **kwargs)

    @classmethod
    def dump_impl(cls, data, config_path, **kwargs):
        """
        :param data: Data to dump :: dict
        :param config_path: Dump destination file path
        :param kwargs: backend-specific optional keyword parameters :: dict
        """
        yaml_dump(data, open(config_path, 'w'), **kwargs)

# vim:sw=4:ts=4:et:
