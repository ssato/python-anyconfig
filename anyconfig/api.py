#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=unused-import,import-error,invalid-name
"""Public APIs of anyconfig module.

.. versionchanged:: 0.2
   Now APIs :func:`find_loader`, :func:`single_load`, :func:`multi_load`,
   :func:`load` and :func:`dump` can process a file/file-like object or a list
   of file/file-like objects instead of a file path or a list of file paths.

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
from anyconfig.utils import get_path_from_stream

# Re-export and aliases:
list_types = anyconfig.backends.list_types  # flake8: noqa
container = anyconfig.mergeabledict.MergeableDict
to_container = container.create


def _is_path(path_or_stream):
    """
    Is given object `path_or_stream` a file path?
    """
    return isinstance(path_or_stream, anyconfig.compat.STR_TYPES)


def _is_paths(maybe_paths):
    """
    Does given object `maybe_paths` consist of path or path pattern strings?
    """
    if anyconfig.utils.is_iterable(maybe_paths):
        return not getattr(maybe_paths, "read", False)

    return False  # Not an iterable at least.


def _maybe_validated(cnf, schema, format_checker=None):
    """
    :param cnf: Configuration object :: container
    :param schema: JSON schema object :: container
    :param format_checker: A format property checker object of which class is
        inherited from jsonschema.FormatChecker, it's default if None given.

    :return: Given `cnf` as it is if validation succeeds else None
    """
    if schema is None:
        return cnf

    (valid, msg) = validate(cnf, schema, format_checker, True)
    if msg:
        LOGGER.warn(msg)

    return cnf if valid else None


def set_loglevel(level):
    """
    :param level: Log level, e.g. logging.INFO and logging.WARN.
    """
    LOGGER.setLevel(level)


def find_loader(path_or_stream, forced_type=None, is_path_=None):
    """
    Find out config parser object appropriate to load from a file of given path
    or file/file-like object.

    :param path_or_stream: Configuration file path or file / file-like object
    :param forced_type: Forced configuration parser type
    :param is_path_: True if given `path_or_stream` is a file path

    :return: Config parser instance or None
    """
    (psr, err) = anyconfig.backends.find_parser(path_or_stream, forced_type,
                                                is_path_=is_path_)
    if psr is None:
        LOGGER.error(err)
        return None

    LOGGER.debug("Using config parser of type: %s", psr.type())
    return psr()  # TBD: Passing initialization arguments.


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
    is_path_ = _is_path(path_or_stream)
    if is_path_:
        path_or_stream = anyconfig.utils.ensure_expandusr(path_or_stream)
        filepath = path_or_stream
    else:
        filepath = get_path_from_stream(path_or_stream)

    psr = find_loader(path_or_stream, forced_type, is_path_)
    if psr is None:
        return None

    schema = format_checker = None
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
            cnf = psr.loads(content, ignore_missing=ignore_missing, **kwargs)
            return _maybe_validated(cnf, schema, format_checker)

        except Exception as exc:
            LOGGER.debug("Exc=%s", str(exc))
            LOGGER.warn("Failed to compile %s, fallback to no template "
                        "mode", path_or_stream)

    cnf = psr.load(path_or_stream, ignore_missing=ignore_missing, **kwargs)
    return _maybe_validated(cnf, schema, format_checker)


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

    :param paths: List of config file paths or a glob pattern to list paths, or
        a list of file/file-like objects
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

    schema = format_checker = None
    if ac_schema is not None:
        kwargs["ac_schema"] = None  # Avoid infinit loop
        format_checker = kwargs.get("format_checker", None)
        schema = load(ac_schema, forced_type=forced_type,
                      ignore_missing=ignore_missing, merge=merge,
                      marker=marker, ac_template=ac_template,
                      ac_context=ac_context, **kwargs)

    cnf = to_container(ac_context) if ac_context else container()

    if _is_path(paths) and marker in paths:
        paths = anyconfig.utils.sglob(paths)

    for path in paths:
        # Nested patterns like ['*.yml', '/a/b/c.yml'].
        if _is_path(path) and marker in path:
            cups = multi_load(path, forced_type=forced_type,
                              ignore_missing=ignore_missing, merge=merge,
                              marker=marker, ac_template=ac_template,
                              ac_context=cnf, **kwargs)
        else:
            cups = single_load(path, forced_type=forced_type,
                               ignore_missing=ignore_missing,
                               ac_template=ac_template, ac_context=cnf,
                               **kwargs)

        cnf.update(cups, merge)

    return _maybe_validated(cnf, schema, format_checker)


def load(path_specs, forced_type=None, ignore_missing=False,
         merge=MS_DICTS, marker='*', ac_template=False, ac_context=None,
         ac_schema=None, **kwargs):
    """
    Load single or multiple config files or multiple config files specified in
    given paths pattern.

    :param path_specs: Configuration file path or paths or its pattern such as
        '/a/b/*.json' or a list of files/file-like objects
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
    if _is_path(path_specs) and marker in path_specs or _is_paths(path_specs):
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

    psr = find_loader(None, forced_type)
    if psr is None:
        return anyconfig.parser.parse(content)

    schema = None
    if ac_schema is not None:
        kwargs["ac_schema"] = None  # Avoid infinit loop
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

    cnf = psr.loads(content, **kwargs)
    return _maybe_validated(cnf, schema, kwargs.get("format_checker", None))


def _find_dumper(path_or_stream, forced_type=None):
    """
    Find configuration parser to dump data.

    :param path_or_stream: Output file path or file / file-like object
    :param forced_type: Forced configuration parser type

    :return: Parser-inherited class object
    """
    psr = find_loader(path_or_stream, forced_type)

    if psr is None or not getattr(psr, "dump", False):
        LOGGER.warn("Dump method not implemented. Fallback to json.Parser")
        psr = anyconfig.backend.json.Parser()

    return psr


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
        LOGGER.info("Dumping: %s", get_path_from_stream(path_or_stream))

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
