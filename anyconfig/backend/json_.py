#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Ref. python -c "import json; help(json)"
#
"""JSON file parser backend.
"""
import anyconfig.backend.base as Base
import anyconfig.compat

try:
    import json
except ImportError:
    import simplejson as json


def dict_to_container(json_obj_dict):
    """Convert dict to container.
    """
    return JsonConfigParser.container().create(json_obj_dict)


_LOAD_OPTS = ["cls", "parse_float", "parse_int", "parse_constant",
              "object_pairs_hook"]

_DUMP_OPTS = ["skipkeys", "ensure_ascii", "check_circular", "allow_nan",
              "cls", "indent", "separators", "default", "sort_keys"]

# It seems that 'encoding' argument is not allowed in json.load[s] and
# json.dump[s] in JSON module in python 3.x.
if not anyconfig.compat.IS_PYTHON_3:
    _LOAD_OPTS.append("encoding")
    _DUMP_OPTS.append("encoding")


class JsonConfigParser(Base.ConfigParser):
    """
    Parser for JSON files.

    - Backend: standard json lib (>= python 2.6) or simplejson
    - Limitations: None obvious
    - Special options:

      - All options of json.load{s,} and json.dump{s,} except object_hook
        should work.
    """
    _type = "json"
    _extensions = ["json", "jsn", "js"]
    _load_opts = _LOAD_OPTS
    _dump_opts = _DUMP_OPTS

    @classmethod
    def loads(cls, config_content, **kwargs):
        """
        :param config_content:  Config file content
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: cls.container() object holding config parameters
        """
        return json.loads(config_content, object_hook=dict_to_container,
                          **Base.mk_opt_args(cls._load_opts, kwargs))

    @classmethod
    def load_impl(cls, config_fp, **kwargs):
        """
        :param config_fp:  Config file object
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: cls.container() object holding config parameters
        """
        return json.load(config_fp, object_hook=dict_to_container, **kwargs)

    @classmethod
    def dumps_impl(cls, data, **kwargs):
        """
        :param data: Data to dump :: dict
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: string represents the configuration
        """
        return json.dumps(data, **kwargs)

    @classmethod
    def dump_impl(cls, data, config_path, **kwargs):
        """
        :param data: Data to dump :: dict
        :param config_path: Dump destination file path
        :param kwargs: backend-specific optional keyword parameters :: dict
        """
        json.dump(data, open(config_path, 'w'), **kwargs)

# vim:sw=4:ts=4:et:
