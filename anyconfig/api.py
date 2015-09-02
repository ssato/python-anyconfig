#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=unused-import,import-error,invalid-name
"""Public APIs of anyconfig module.

.. versionadded:: 0.2
   Export factory method (create) of anyconfig.mergeabledict.MergeableDict
"""
from __future__ import absolute_import

import os.path

from anyconfig.globals import LOGGER
import anyconfig.backends
import anyconfig.backend.json
import anyconfig.compat
import anyconfig.mergeabledict
import anyconfig.parser
import anyconfig.template
import anyconfig.utils

# Import some global constants will be re-exported:
from anyconfig.mergeabledict import (
    MS_REPLACE, MS_NO_REPLACE, MS_DICTS, MS_DICTS_AND_LISTS, MERGE_STRATEGIES,
    get, set_  # flake8: noqa
)
from anyconfig.parser import PATH_SEPS
from anyconfig.schema import validate, gen_schema

# Re-export and aliases:
list_types = anyconfig.backends.list_types  # flake8: noqa
container = anyconfig.mergeabledict.MergeableDict
to_container = container.create


def _is_path(path_or_stream):
    """
    Is given object `path_or_stream` a file path?
    """
    return isinstance(path_or_stream, anyconfig.compat.STR_TYPES)


def _get_path_from_stream(stream):
    """
    Try to get file path from given stream `stream`.
    """
    maybe_path = getattr(stream, "name", None)
    if maybe_path is not None:
        maybe_path = os.path.abspath(maybe_path)

    return maybe_path


def _validate(cnf, schema, format_checker=None):
    """
    Wrapper function for anycnf.schema.vaildate.

    :param cnf: Configuration object :: container
    :param schema: JSON schema object :: container
    :param format_checker: A format property checker object of which class is
        inherited from jsonschema.FormatChecker, it's default if None given.

    :return: True if validation suceeds or jsonschema module is not available.
    """
    (ret, msg) = validate(cnf, schema, format_checker, True)
    if msg:
        LOGGER.warn(msg)

    return ret


def set_loglevel(level):
    """
    :param level: Log level, e.g. logging.INFO and logging.WARN.
    """
    LOGGER.setLevel(level)


def find_loader(path_or_stream, forced_type=None):
    """
    Find out config parser object appropriate to load from a file of given path
    or file/file-like object.

    :param path_or_stream: Configuration file path or file / file-like object
    :param forced_type: Forced configuration parser type

    :return: Config parser instance or None
    """
    if forced_type is not None:
        cparser = anyconfig.backends.find_by_type(forced_type)
        if not cparser:
            LOGGER.error("No parser found for given type: %s", forced_type)
            return None
    else:
        if not _is_path(path_or_stream):
            path_or_stream = _get_path_from_stream(path_or_stream)
            if path_or_stream is None:
                return None  # No way to detect filename.

        cparser = anyconfig.backends.find_by_file(path_or_stream)
        if not cparser:
            LOGGER.error("No parser found for given file: %s", path_or_stream)
            return None

    LOGGER.debug("Using config parser of type: %s", cparser.type())
    return cparser()


def single_load(path_or_stream, forced_type=None, ignore_missing=False,
                ac_template=False, ac_context=None, ac_schema=None,
                **kwargs):
    """
    Load single config file.

    :param path_or_stream: Configuration file path or file / file-like object
    :param forced_type: Forced configuration parser type
    :param ignore_missing: Ignore and just return empty result if given file
        (``path_or_stream``) does not exist
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
    if _is_path(path_or_stream):
        path_or_stream = anyconfig.utils.ensure_expandusr(path_or_stream)
        filepath = path_or_stream
    else:
        filepath = _get_path_from_stream(path_or_stream)

    cparser = find_loader(path_or_stream, forced_type)
    if cparser is None:
        return None

    if ac_schema is not None:
        kwargs["ac_schema"] = None  # Avoid infinit loop
        format_checker = kwargs.get("format_checker", None)
        LOGGER.info("Loading schema: %s", ac_schema)
        schema = load(ac_schema, forced_type=forced_type,
                      ignore_missing=ignore_missing, ac_template=ac_template,
                      ac_context=ac_context, **kwargs)

    LOGGER.info("Loading: %s", filepath)
    if ac_template and filepath is not None:
        try:
            LOGGER.debug("Compiling: %s", filepath)
            content = anyconfig.template.render(filepath, ac_context)
            config = cparser.loads(content, ignore_missing=ignore_missing,
                                   **kwargs)
            if ac_schema is not None:
                if not _validate(config, schema, format_checker):
                    return None

            return config

        except Exception as exc:
            LOGGER.debug("Exc=%s", str(exc))
            LOGGER.warn("Failed to compile %s, fallback to no template "
                        "mode", path_or_stream)

    config = cparser.load(path_or_stream, ignore_missing=ignore_missing, **kwargs)

    if ac_schema is not None:
        if not _validate(config, schema, format_checker):
            return None

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

    if not paths:
        return container()

    if ac_schema is not None:
        kwargs["ac_schema"] = None  # Avoid infinit loop
        format_checker = kwargs.get("format_checker", None)
        schema = load(ac_schema, forced_type=forced_type,
                      ignore_missing=ignore_missing, merge=merge,
                      marker=marker, ac_template=ac_template,
                      ac_context=ac_context, **kwargs)

    config = to_container(ac_context) if ac_context else container()

    if _is_path(paths) and marker in paths:
        paths = anyconfig.utils.sglob(paths)

    for path in paths:
        # Nested patterns like ['*.yml', '/a/b/c.yml'].
        if _is_path(path) and marker in path:
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
        if not _validate(config, schema, format_checker):
            return None

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
    if (_is_path(path_specs) and marker in path_specs) or \
        anyconfig.utils.is_iterable(path_specs):
        return multi_load(path_specs, forced_type=forced_type,
                          ignore_missing=ignore_missing, merge=merge,
                          marker=marker, ac_template=ac_template,
                          ac_context=ac_context, ac_schema=ac_schema, **kwargs)
    else:
        return single_load(path_specs, forced_type=forced_type,
                           ignore_missing=ignore_missing,
                           ac_template=ac_template, ac_context=ac_context,
                           ac_schema=ac_schema, **kwargs)


def loads(content, forced_type=None, ac_template=False, ac_context=None,
          ac_schema=None, **kwargs):
    """
    :param content: Configuration file's content
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
        LOGGER.warn("No config type was given. Try to parse...")
        return anyconfig.parser.parse(content)

    cparser = find_loader(None, forced_type)
    if cparser is None:
        return anyconfig.parser.parse(content)

    if ac_schema is not None:
        kwargs["ac_schema"] = None  # Avoid infinit loop
        format_checker = kwargs.get("format_checker", None)
        schema = loads(ac_schema, forced_type, ac_template, ac_context,
                       **kwargs)

    if ac_template:
        try:
            LOGGER.debug("Compiling")
            content = anyconfig.template.render_s(content, ac_context)
        except Exception as exc:
            LOGGER.debug("Exc=%s", str(exc))
            LOGGER.warn("Failed to compile and fallback to no template "
                        "mode: '%s'", content[:50] + '...')

    cnf = cparser.loads(content, **kwargs)

    if ac_schema is not None:
        if not _validate(cnf, schema, format_checker):
            LOGGER.warn("Validation failed: schema=%s", schema)
            return None

    return cnf


def _find_dumper(path_or_stream, forced_type=None):
    """
    Find configuration parser to dump data.

    :param path_or_stream: Output file path or file / file-like object
    :param forced_type: Forced configuration parser type

    :return: Parser-inherited class object
    """
    cparser = find_loader(path_or_stream, forced_type)

    if cparser is None or not getattr(cparser, "dump", False):
        LOGGER.warn("Dump method not implemented. Fallback to json.Parser")
        cparser = anyconfig.backend.json.Parser()

    return cparser


def dump(data, path_or_stream, forced_type=None, **kwargs):
    """
    Save `data` as `path_or_stream`.

    :param data: Config data object to dump ::
        anyconfig.mergeabledict.MergeableDict by default
    :param path_or_stream: Output file path or file / file-like object
    :param forced_type: Forced configuration parser type
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend
    """
    dumper = _find_dumper(path_or_stream, forced_type)

    if _is_path(path_or_stream):
        LOGGER.info("Dumping: %s", path_or_stream)
    else:
        LOGGER.info("Dumping: %s", _get_path_from_stream(path_or_stream))

    dumper.dump(data, path_or_stream, **kwargs)


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
