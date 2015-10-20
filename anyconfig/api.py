#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=unused-import,import-error,invalid-name
"""Public APIs of anyconfig module.

.. versionchanged:: 0.3
   Replaced `forced_type` optional argument of some public APIs with
   `ac_parser` to allow skip of config parser search by passing parser object
   previously found and instantiated.

   Also removed some optional arguments, `ignore_missing`, `merge` and
   `marker`, from definitions of some public APIs as these may not be changed
   from default in common use cases.

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
from anyconfig.utils import is_path

# Re-export and aliases:
list_types = anyconfig.backends.list_types  # flake8: noqa
container = anyconfig.mergeabledict.MergeableDict
to_container = container.create


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


def find_loader(path_or_stream, parser_or_type=None, is_path_=None):
    """
    Find out config parser object appropriate to load from a file of given path
    or file/file-like object.

    :param path_or_stream: Configuration file path or file / file-like object
    :param parser_or_type: Forced configuration parser type or parser object
    :param is_path_: True if given `path_or_stream` is a file path

    :return: Config parser instance or None
    """
    if anyconfig.backends.is_parser(parser_or_type):
        return parser_or_type

    (psr, err) = anyconfig.backends.find_parser(path_or_stream, parser_or_type,
                                                is_path_=is_path_)
    if psr is None:
        LOGGER.error(err)
        return None

    LOGGER.debug("Using config parser: %r [%s]", psr, psr.type())
    return psr()  # TBD: Passing initialization arguments.


def single_load(path_or_stream, ac_parser=None, ac_template=False,
                ac_context=None, ac_schema=None, **kwargs):
    """
    Load single config file.

    :param path_or_stream: Configuration file path or file / file-like object
    :param ac_parser: Forced parser type or parser object
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: A dict presents context to instantiate template
    :param ac_schema: JSON schema file path to validate given config file
    :param kwargs: Optional keyword arguments for backends:

        - Common backend options:

          - ignore_missing: Ignore and just return empty result if given file
            (``path_or_stream``) does not exist.

        - Backend specific options such as {"indent": 2} for JSON backend

    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    is_path_ = is_path(path_or_stream)
    if is_path_:
        path_or_stream = anyconfig.utils.ensure_expandusr(path_or_stream)
        filepath = path_or_stream
    else:
        filepath = anyconfig.utils.get_path_from_stream(path_or_stream)

    psr = find_loader(path_or_stream, ac_parser, is_path_)
    if psr is None:
        return None

    schema = format_checker = None
    if ac_schema is not None:
        kwargs["ac_schema"] = None  # Avoid infinit loop
        format_checker = kwargs.get("format_checker", None)
        LOGGER.info("Loading schema: %s", ac_schema)
        schema = load(ac_schema, ac_parser=None, ac_template=ac_template,
                      ac_context=ac_context, **kwargs)

    LOGGER.info("Loading: %s", filepath)
    if ac_template and filepath is not None:
        try:
            LOGGER.debug("Compiling: %s", filepath)
            content = anyconfig.template.render(filepath, ac_context)
            cnf = psr.loads(content, **kwargs)
            return _maybe_validated(cnf, schema, format_checker)

        except Exception as exc:
            LOGGER.warn("Failed to compile %s, fallback to no template "
                        "mode, exc=%s", path_or_stream, str(exc))

    cnf = psr.load(path_or_stream, **kwargs)
    return _maybe_validated(cnf, schema, format_checker)


def multi_load(paths, ac_parser=None, ac_template=False, ac_context=None,
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
    :param ac_parser: Forced parser type or parser object
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: A dict presents context to instantiate template
    :param ac_schema: JSON schema file path to validate given config file
    :param kwargs: Optional keyword arguments:

        - Common options:

          - ac_merge (merge): Specify strategy of how to merge results loaded
            from multiple configuration files. See the doc of mergeabledict
            module for more details of strategies. The default is MS_DICTS.

          - ac_marker (marker): Globbing marker to detect paths patterns.

        - Common backend options:

          - ignore_missing: Ignore and just return empty result if given file
            (``path_or_stream``) does not exist.

        - Backend specific options such as {"indent": 2} for JSON backend

    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    marker = kwargs.setdefault("ac_marker", kwargs.get("marker", '*'))
    ac_merge = kwargs.setdefault("ac_merge", kwargs.get("merge", MS_DICTS))
    if ac_merge not in MERGE_STRATEGIES:
        raise ValueError("Invalid merge strategy: " + ac_merge)

    schema = format_checker = None
    if ac_schema is not None:
        kwargs["ac_schema"] = None  # Avoid infinit loop
        format_checker = kwargs.get("format_checker", None)
        schema = load(ac_schema, ac_parser=None, ac_template=ac_template,
                      ac_context=ac_context, **kwargs)

    cnf = to_container(ac_context) if ac_context else container()
    same_type = anyconfig.utils.are_same_file_types(paths)

    if is_path(paths) and marker in paths:
        paths = anyconfig.utils.sglob(paths)

    for path in paths:
        # Nested patterns like ['*.yml', '/a/b/c.yml'].
        if is_path(path) and marker in path:
            cups = multi_load(path, ac_parser=ac_parser,
                              ac_template=ac_template, ac_context=cnf,
                              **kwargs)
        else:
            if same_type:
                ac_parser = find_loader(path, ac_parser, is_path(path))
            cups = single_load(path, ac_parser=ac_parser,
                               ac_template=ac_template, ac_context=cnf,
                               **kwargs)

        cnf.update(cups, ac_merge)

    return _maybe_validated(cnf, schema, format_checker)


def load(path_specs, ac_parser=None, ac_template=False, ac_context=None,
         ac_schema=None, **kwargs):
    """
    Load single or multiple config files or multiple config files specified in
    given paths pattern.

    :param path_specs: Configuration file path or paths or its pattern such as
        '/a/b/\*.json' or a list of files/file-like objects
    :param ac_parser: Forced parser type or parser object
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: A dict presents context to instantiate template
    :param ac_schema: JSON schema file path to validate given config file
    :param kwargs:
        Optional keyword arguments. See also the description of `kwargs` in
        `multi_load` function.

    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    marker = kwargs.setdefault("ac_marker", kwargs.get("marker", '*'))

    if is_path(path_specs) and marker in path_specs or _is_paths(path_specs):
        return multi_load(path_specs, ac_parser=ac_parser,
                          ac_template=ac_template, ac_context=ac_context,
                          ac_schema=ac_schema, **kwargs)
    else:
        return single_load(path_specs, ac_parser=ac_parser,
                           ac_template=ac_template, ac_context=ac_context,
                           ac_schema=ac_schema, **kwargs)


def loads(content, ac_parser=None, ac_template=False, ac_context=None,
          ac_schema=None, **kwargs):
    """
    :param content: Configuration file's content
    :param ac_parser: Forced parser type or parser object
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
    if ac_parser is None:
        LOGGER.warn("No type or parser was given. Try to parse...")
        return anyconfig.parser.parse(content)

    psr = find_loader(None, ac_parser)
    if psr is None:
        return anyconfig.parser.parse(content)

    schema = None
    if ac_schema is not None:
        kwargs["ac_schema"] = None  # Avoid infinit loop
        schema = loads(ac_schema, psr, ac_template, ac_context, **kwargs)

    if ac_template:
        try:
            LOGGER.debug("Compiling")
            content = anyconfig.template.render_s(content, ac_context)
        except Exception as exc:
            LOGGER.warn("Failed to compile and fallback to no template "
                        "mode: '%s', exc=%s", content[:50] + '...', str(exc))

    cnf = psr.loads(content, **kwargs)
    return _maybe_validated(cnf, schema, kwargs.get("format_checker", None))


def _find_dumper(path_or_stream, ac_parser=None):
    """
    Find configuration parser to dump data.

    :param path_or_stream: Output file path or file / file-like object
    :param ac_parser: Forced parser type or parser object

    :return: Parser-inherited class object
    """
    psr = find_loader(path_or_stream, ac_parser)

    if psr is None or not getattr(psr, "dump", False):
        LOGGER.warn("Dump method not implemented. Fallback to json.Parser")
        psr = anyconfig.backend.json.Parser()

    return psr


def dump(data, path_or_stream, ac_parser=None, **kwargs):
    """
    Save `data` as `path_or_stream`.

    :param data: Config data object to dump ::
        anyconfig.mergeabledict.MergeableDict by default
    :param path_or_stream: Output file path or file / file-like object
    :param ac_parser: Forced parser type or parser object
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend
    """
    dumper = _find_dumper(path_or_stream, ac_parser)
    LOGGER.info("Dumping: %s",
                anyconfig.utils.get_path_from_stream(path_or_stream))
    dumper.dump(data, path_or_stream, **kwargs)


def dumps(data, ac_parser=None, **kwargs):
    """
    Return string representation of `data` in forced type format.

    :param data: Config data object to dump ::
        anyconfig.mergeabledict.MergeableDict by default
    :param ac_parser: Forced parser type or parser object
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend

    :return: Backend-specific string representation for the given data
    """
    return _find_dumper(None, ac_parser).dumps(data, **kwargs)

# vim:sw=4:ts=4:et:
