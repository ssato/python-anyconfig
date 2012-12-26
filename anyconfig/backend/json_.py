#
# Copyright (C) 2011, 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.base as Base

import logging
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


def dict_to_container(json_obj_dict):
    return JsonConfigParser.container()(**json_obj_dict)


class JsonConfigParser(Base.ConfigParser):
    _type = "json"
    _extensions = ["json", "jsn"]

    @classmethod
    def loads(cls, config_content, *args, **kwargs):
        return json.loads(config_content, object_hook=dict_to_container)

    @classmethod
    def load(cls, config_path, *args, **kwargs):
        return json.load(open(config_path), object_hook=dict_to_container)

    @classmethod
    def dumps(cls, data, *args, **kwargs):
        return json.dumps(data, indent=2)

    @classmethod
    def dump(cls, data, config_path, *args, **kwargs):
        json.dump(data, open(config_path, "w"), indent=2)


# vim:sw=4:ts=4:et:
