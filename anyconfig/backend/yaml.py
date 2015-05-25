#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""YAML files parser backend
"""
from __future__ import absolute_import

import yaml
import anyconfig.backend.base as Base


def filter_keys(keys, filter_key):
    """
    :param keys: Original keys list
    :param filter_key: Key to filter out from `keys`
    :return: A list of keys given `filter_key` is not contained
    """
    return [k for k in keys if k != filter_key]


def yaml_load(fpath, **kwargs):
    """
    An wrapper of yaml.{safe_,}load
    """
    keys = filter_keys(kwargs.keys(), "safe")
    if kwargs.get("safe", False):
        return yaml.safe_load(fpath, **Base.mk_opt_args(keys, kwargs))
    else:
        return yaml.load(fpath, **kwargs)


def yaml_dump(data, fpath, **kwargs):
    """
    An wrapper of yaml.{safe_,}dump
    """
    keys = filter_keys(kwargs.keys(), "safe")
    if kwargs.get("safe", False):
        return yaml.safe_dump(data, fpath, **Base.mk_opt_args(keys, kwargs))
    else:
        return yaml.dump(data, fpath, **kwargs)


class Parser(Base.Parser):
    """
    Parser for YAML files.

    - Backend: PyYAML (yaml)
    - Limitations: None obvious
    - Special options:

      - All options of yaml.{safe_,}load and yaml.{safe_,}dump should work.
      - Use 'safe' boolean keyword option if you prefer yaml.safe_{load,dump}
        instead of yaml.{load,dump}
    """

    _type = "yaml"
    _extensions = ("yaml", "yml")
    _load_opts = ["Loader", "safe"]
    _dump_opts = ["stream", "Dumper"]

    @classmethod
    def load_impl(cls, config_content, **kwargs):
        """
        :param config_content:  Config file content
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: dict object holding config parameters
        """
        return yaml_load(config_content, **kwargs)

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
