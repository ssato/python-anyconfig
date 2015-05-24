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


SUPPORTED = True
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise RuntimeError("Necessary JSON module is not available!")


def dict_to_container(json_obj_dict):
    """Convert dict to container.
    """
    return JsonConfigParser.container().create(json_obj_dict)


_LOAD_OPTS = ["cls", "object_hook", "parse_float", "parse_int",
              "parse_constant", "object_pairs_hook"]

_DUMP_OPTS = ["skipkeys", "ensure_ascii", "check_circular", "allow_nan",
              "cls", "indent", "separators", "default", "sort_keys"]

# It seems that 'encoding' argument is not allowed in json.load[s] and
# json.dump[s] in JSON module in python 3.x.
if not anyconfig.compat.IS_PYTHON_3:
    _LOAD_OPTS.append("encoding")
    _DUMP_OPTS.append("encoding")


class JsonConfigParser(Base.ConfigParser):
    """
    JSON files parser.
    """
    _type = "json"
    _extensions = ["json", "jsn", "js"]
    _supported = SUPPORTED

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
    def load(cls, config_path, ignore_missing=False, **kwargs):
        """
        :param config_path:  Config file path
        :param ignore_missing: Ignore just return empty result if given file
            (``config_path``) does not exist
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: cls.container() object holding config parameters
        """
        # NOTE: Hack. See also: :method:``load`` of the class
        # :class:``anyconfig.backends.Base.ConfigParser``.
        if ignore_missing and not cls.exists(config_path):
            return cls.container()()

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
