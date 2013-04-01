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

    @classmethod
    def loads(cls, config_content, **kwargs):
        return json.loads(config_content, object_hook=dict_to_container,
                          **Base.mk_opt_args(_LOAD_OPTS, kwargs))

    @classmethod
    def load(cls, config_path, **kwargs):
        return json.load(open(config_path), object_hook=dict_to_container,
                         **Base.mk_opt_args(_LOAD_OPTS, kwargs))

    @classmethod
    def dumps(cls, data, **kwargs):
        return json.dumps(data, **Base.mk_opt_args(_DUMP_OPTS, kwargs))

    @classmethod
    def dump(cls, data, config_path, **kwargs):
        json.dump(data, open(config_path, "w"),
                  **Base.mk_opt_args(_DUMP_OPTS, kwargs))


# vim:sw=4:ts=4:et:
