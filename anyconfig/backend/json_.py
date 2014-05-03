#
# Copyright (C) 2011 - 2014 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Ref. python -c "import json; help(json)"
#
import anyconfig.backend.base as Base
import sys


SUPPORTED = True
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise RuntimeError("Necessary JSON module is not available!")


def dict_to_container(json_obj_dict):
    return JsonConfigParser.container().create(json_obj_dict)


class JsonConfigParser(Base.ConfigParser):
    _type = "json"
    _extensions = ["json", "jsn", "js"]
    _supported = SUPPORTED

    _load_opts = ["encoding", "cls", "object_hook", "parse_float", "parse_int",
                  "parse_constant", "object_pairs_hook"]
    _dump_opts = ["skipkeys", "ensure_ascii", "check_circular", "allow_nan",
                  "cls", "indent", "separators", "encoding", "default",
                  "sort_keys"]

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
    def load(cls, config_path, **kwargs):
        """
        :param config_path:  Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: cls.container() object holding config parameters
        """
        return json.load(open(config_path), object_hook=dict_to_container,
                         **Base.mk_opt_args(cls._load_opts, kwargs))

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
