#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=unused-import,import-error,invalid-name
"""Public APIs of anyconfig module.
"""
from __future__ import absolute_import

try:
    import jsonschema
except ImportError:
    pass

from anyconfig.globals import LOGGER
import anyconfig.backends
import anyconfig.backend.json
import anyconfig.compat
import anyconfig.mergeabledict
import anyconfig.parser
import anyconfig.template
import anyconfig.utils

# Import some global constants will be re-exported:
from anyconfig.mergeabledict import MS_REPLACE, MS_NO_REPLACE, \
    MS_DICTS, MS_DICTS_AND_LISTS, MERGE_STRATEGIES, \
    get, set_  # flake8: noqa
from anyconfig.parser import PATH_SEPS

# Re-export and aliases:
list_types = anyconfig.backends.list_types  # flake8: noqa
container = anyconfig.mergeabledict.MergeableDict


class ValidationError(Exception):
    pass


def set_loglevel(level):
    """
    :param level: Log level, e.g. logging.INFO and logging.WARN.
    """
    LOGGER.setLevel(level)


def find_loader(config_path, forced_type=None):
    """
    :param config_path: Configuration file path
    :param forced_type: Forced configuration parser type

    :return: Parser-inherited class object
    """
    if forced_type is not None:
        cparser = anyconfig.backends.find_by_type(forced_type)
        if not cparser:
            LOGGER.error("No parser found for given type: %s", forced_type)
            return None
    else:
        cparser = anyconfig.backends.find_by_file(config_path)
        if not cparser:
            LOGGER.error("No parser found for given file: %s", config_path)
            return None

    LOGGER.debug("Using config parser of type: %s", cparser.type())
    return cparser


def validate(config, schema, format_checker=None):
    """
    Validate config object with given schema object, loaded from JSON schema.

    See also: https://python-jsonschema.readthedocs.org/en/latest/validate/

    :param config: Config object (a dict or a dict-like object) to validate
    :param schema: Schema object (a dict or a dict-like object)
        instantiated from schema JSON file or schema JSON string
    :param format_checker: A format property checker object of which class is
        inherited from jsonschema.FormatChecker, it's default if None given.

    :return: (True if validation succeeded else False, error message)
    """
    try:
        if format_checker is None:
            format_checker = jsonschema.FormatChecker()  # :throw: NameError
        try:
            jsonschema.validate(config, schema, format_checker=format_checker)
        except (jsonschema.ValidationError, jsonschema.SchemaError) as exc:
            return (False, str(exc))

    except NameError:
        return (True, "Validation module (jsonschema) is not available")

    return (True, '')


def _validate(config, schema, format_checker=None):
    """
    Validate config object with given schema object, loaded from JSON schema.

    See also: https://python-jsonschema.readthedocs.org/en/latest/validate/

    :param config: Config object (a dict or a dict-like object) to validate
    :param schema: Schema object (a dict or a dict-like object)
        instantiated from schema JSON file or schema JSON string
    :param format_checker: A format property checker object of which class is
        inherited from jsonschema.FormatChecker, it's default if None given.

    :return: True if validation succeeded else False
    """
    (rc, msg) = validate(config, schema, format_checker)
    if msg:
        LOGGER.warn(msg)
    if not rc:
        raise ValidationError(msg)

    return True


def single_load(config_path, forced_type=None, ignore_missing=False,
                ac_template=False, ac_context=None, ac_schema=None,
                **kwargs):
    """
    Load single config file.

    :param config_path: Configuration file path
    :param forced_type: Forced configuration parser type
    :param ignore_missing: Ignore and just return empty result if given file
        (``config_path``) does not exist
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: A dict presents context to instantiate template
    :param ac_schema: JSON schema file path to validate given config file
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend

    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    config_path = anyconfig.utils.ensure_expandusr(config_path)

    cparser = find_loader(config_path, forced_type)
    if cparser is None:
        return None

    if ac_schema is not None:
        kwargs["ac_schema"] = None  # Avoid infinit loop
        format_checker = kwargs.get("format_checker", None)
        schema = load(ac_schema, forced_type, ignore_missing, ac_template,
                      ac_context, **kwargs)

    LOGGER.info("Loading: %s", config_path)
    if ac_template:
        try:
            LOGGER.debug("Compiling: %s", config_path)
            config_content = anyconfig.template.render(config_path, ac_context)
            config = cparser.loads(config_content, ignore_missing=ignore_missing,
                                 **kwargs)
            if ac_schema is not None:
                if _validate(config, schema, format_checker):
                    return config

            return config

        except Exception as exc:
            LOGGER.debug("Exc=%s", str(exc))
            LOGGER.warn("Failed to compile %s, fallback to no template "
                        "mode", config_path)

    config = cparser.load(config_path, ignore_missing=ignore_missing,
                          **kwargs)

    if ac_schema is not None:
        if _validate(config, schema, format_checker):
            return config

    return config


def multi_load(paths, forced_type=None, ignore_missing=False,
               merge=MS_DICTS, marker='*', ac_template=False, ac_context=None,
               ac_schema=None, **kwargs):
    """
    Load multiple config files.

    The first argument `paths` may be a list of config file paths or
    a glob pattern specifying that. That is, if a.yml, b.yml and c.yml are in
    the dir /etc/foo/conf.d/, the followings give same results::

      multi_load(["/etc/foo/conf.d/a.yml", "/etc/foo/conf.d/b.yml",
                  "/etc/foo/conf.d/c.yml", ])

      multi_load("/etc/foo/conf.d/*.yml")

    :param paths: List of config file paths or a glob pattern to list paths
    :param forced_type: Forced configuration parser type
    :param ignore_missing: Ignore missing config files
    :param merge: Strategy to merge config results of multiple config files
        loaded. see also: anyconfig.mergeabledict.MergeableDict.update()
    :param marker: Globbing markerer to detect paths patterns
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: A dict presents context to instantiate template
    :param ac_schema: JSON schema file path to validate given config file
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend

    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    if merge not in MERGE_STRATEGIES:
        raise ValueError("Invalid merge strategy: " + merge)

    if marker in paths:
        paths = anyconfig.utils.sglob(paths)

    if ac_schema is not None:
        kwargs["ac_schema"] = None  # Avoid infinit loop
        format_checker = kwargs.get("format_checker", None)
        schema = load(ac_schema, forced_type, ignore_missing, merge,
                      marker, ac_template, ac_context, **kwargs)

    config = container.create(ac_context) if ac_context else container()
    for path in paths:
        if marker in path:  # Nested patterns like ['*.yml', '/a/b/c.yml'].
            conf_updates = multi_load(path, forced_type=forced_type,
                                      ignore_missing=ignore_missing,
                                      merge=merge, marker=marker,
                                      ac_template=ac_template,
                                      ac_context=config, **kwargs)
        else:
            conf_updates = single_load(path, forced_type=forced_type,
                                       ignore_missing=ignore_missing,
                                       ac_template=ac_template,
                                       ac_context=config, **kwargs)

        config.update(conf_updates, merge)

    if ac_schema is not None:
        if _validate(config, schema, format_checker):
            return config

    return config


def load(path_specs, forced_type=None, ignore_missing=False,
         merge=MS_DICTS, marker='*', ac_template=False, ac_context=None,
         ac_schema=None, **kwargs):
    """
    Load single or multiple config files or multiple config files specified in
    given paths pattern.

    :param path_specs:
        Configuration file path or paths or its pattern such as '/a/b/*.json'
    :param forced_type: Forced configuration parser type
    :param ignore_missing: Ignore missing config files
    :param merge: Merging strategy to use
    :param marker: Globbing marker to detect paths patterns
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: A dict presents context to instantiate template
    :param ac_schema: JSON schema file path to validate given config file
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend

    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    if marker in path_specs or anyconfig.utils.is_iterable(path_specs):
        return multi_load(path_specs, forced_type, ignore_missing,
                          merge, marker, ac_template, ac_context, ac_schema,
                          **kwargs)
    else:
        return single_load(path_specs, forced_type, ignore_missing,
                           ac_template, ac_context, ac_schema, **kwargs)


def loads(config_content, forced_type=None, ac_template=False, ac_context=None,
          ac_schema=None, **kwargs):
    """
    :param config_content: Configuration file's content
    :param forced_type: Forced configuration parser type
    :param ignore_missing: Ignore missing config files
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: Context dict to instantiate template
    :param ac_schema: JSON schema content to validate given config file
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend

    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    if forced_type is None:
        return anyconfig.parser.parse(config_content)

    cparser = find_loader(None, forced_type)
    if cparser is None:
        return anyconfig.parser.parse(config_content)

    if ac_schema is not None:
        kwargs["ac_schema"] = None  # Avoid infinit loop
        format_checker = kwargs.get("format_checker", None)
        schema = loads(ac_schema, forced_type, ac_template, ac_context,
                       **kwargs)

    if ac_template:
        try:
            LOGGER.debug("Compiling")
            config_content = anyconfig.template.render_s(config_content,
                                                         ac_context)
        except Exception as exc:
            LOGGER.debug("Exc=%s", str(exc))
            LOGGER.warn("Failed to compile and fallback to no template "
                        "mode: '%s'", config_content[:50] + '...')

    config = cparser.loads(config_content, **kwargs)

    if ac_schema is not None:
        if _validate(config, schema, format_checker):
            return config

    return config


def _find_dumper(config_path, forced_type=None):
    """
    Find configuration parser to dump data.

    :param config_path: Output filename
    :param forced_type: Forced configuration parser type

    :return: Parser-inherited class object
    """
    cparser = find_loader(config_path, forced_type)

    if cparser is None or not getattr(cparser, "dump", False):
        LOGGER.warn("Dump method not implemented. Fallback to json.Parser")
        cparser = anyconfig.backend.json.Parser()

    return cparser


def dump(data, config_path, forced_type=None, **kwargs):
    """
    Save `data` as `config_path`.

    :param data: Config data object to dump ::
        anyconfig.mergeabledict.MergeableDict by default
    :param config_path: Output filename
    :param forced_type: Forced configuration parser type
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend
    """
    dumper = _find_dumper(config_path, forced_type)

    LOGGER.info("Dumping: %s", config_path)
    dumper.dump(data, config_path, **kwargs)


def dumps(data, forced_type, **kwargs):
    """
    Return string representation of `data` in forced type format.

    :param data: Config data object to dump ::
        anyconfig.mergeabledict.MergeableDict by default
    :param forced_type: Forced configuration parser type
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend

    :return: Backend-specific string representation for the given data
    """
    return _find_dumper(None, forced_type).dumps(data, **kwargs)

# vim:sw=4:ts=4:et:
