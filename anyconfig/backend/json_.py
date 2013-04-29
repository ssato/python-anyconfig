#
# Copyright (C) 2011 - 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
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
        sys.stderr.write(
            "JSON module is not available. Disabled its support.\n"
        )
        SUPPORTED = False


_LOAD_OPTS = ["cls", "parse_float", "parse_int", "parse_constant"]
_DUMP_OPTS = ["cls", "skipkeys", "ensure_ascii", "check_circular", "allow_nan",
              "indent", "separators"]


def dict_to_container(json_obj_dict):
    return JsonConfigParser.container().create(json_obj_dict)


class JsonConfigParser(Base.ConfigParser):
    _type = "json"
    _extensions = ["json", "jsn"]
    _supported = SUPPORTED

    _load_opts = _LOAD_OPTS
    _dump_opts = _DUMP_OPTS

    @classmethod
    def loads(cls, config_content, **kwargs):
        return json.loads(config_content, object_hook=dict_to_container,
                          **Base.mk_opt_args(cls._load_opts, kwargs))

    @classmethod
    def load(cls, config_path, **kwargs):
        return json.load(open(config_path), object_hook=dict_to_container,
                         **Base.mk_opt_args(cls._load_opts, kwargs))

    @classmethod
    def dumps_impl(cls, data, **kwargs):
        return json.dumps(data, **kwargs)

    @classmethod
    def dump_impl(cls, data, config_path, **kwargs):
        """
        :param data: Data to dump :: dict
        :param config_path: Dump destination file path
        """
        return json.dump(data, open(config_path, 'w'), **kwargs)

# vim:sw=4:ts=4:et:
