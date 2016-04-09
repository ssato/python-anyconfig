#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=unused-import,import-error,invalid-name
r"""Public APIs of anyconfig module.

.. versionadded:: 0.5.0
   - Most keyword arguments passed to APIs are now position independent.
   - Added ac_namedtuple parameter to \*load and \*dump APIs.

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
import anyconfig.mdicts
import anyconfig.template
import anyconfig.utils

# Import some global constants will be re-exported:
from anyconfig.mdicts import (
    MS_REPLACE, MS_NO_REPLACE, MS_DICTS, MS_DICTS_AND_LISTS, MERGE_STRATEGIES,
    get, set_, to_container  # flake8: noqa
)
from anyconfig.schema import validate, gen_schema
from anyconfig.utils import is_path

# Re-export and aliases:
list_types = anyconfig.backends.list_types  # flake8: noqa


def _is_paths(maybe_paths):
    """
    Does given object `maybe_paths` consist of path or path pattern strings?
    """
    if anyconfig.utils.is_iterable(maybe_paths):
        return not getattr(maybe_paths, "read", False)

    return False  # Not an iterable at least.


def _maybe_validated(cnf, schema, format_checker=None, **options):
    """
    :param cnf: Configuration object
    :param schema: JSON schema object
    :param format_checker: A format property checker object of which class is
        inherited from jsonschema.FormatChecker, it's default if None given.
    :param options: Keyword options such as:

        - ac_namedtuple: Convert result to nested namedtuple object if True

    :return: Given `cnf` as it is if validation succeeds else None
    """
    valid = True
    if schema:
        (valid, msg) = validate(cnf, schema, format_checker=format_checker,
                                safe=True)
        if msg:
            LOGGER.warning(msg)

    if valid:
        if options.get("ac_namedtuple", False):
            return anyconfig.mdicts.convert_to(cnf, ac_namedtuple=True)
        else:
            return cnf

    return None


def set_loglevel(level):
    """
    :param level: Log level, e.g. logging.INFO and logging.WARN.
    """
    LOGGER.setLevel(level)


def find_loader(path_or_stream, parser_or_type=None, is_path_=False):
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
    if err:
        LOGGER.error(err)

    if psr is None:
        if parser_or_type is None:
            LOGGER.warning("No parser (type) was given!")
        else:
            LOGGER.warning("Parser %s was not found!", str(parser_or_type))
        return None

    LOGGER.debug("Using config parser: %r [%s]", psr, psr.type())
    return psr()  # TBD: Passing initialization arguments.


def _load_schema(**options):
    """
    :param options: Optional keyword arguments such as

        - ac_template: Assume configuration file may be a template file and try
          to compile it AAR if True
        - ac_context: A dict presents context to instantiate template
        - ac_schema: JSON schema file path to validate given config file
    """
    ac_schema = options.get("ac_schema", None)
    if ac_schema is not None:
        # Try to detect the appropriate as it may be different from the
        # original config file's format, perhaps.
        options["ac_parser"] = None
        options["ac_schema"] = None  # Avoid infinite loop.
        LOGGER.info("Loading schema: %s", ac_schema)
        return load(ac_schema, **options)

    return None


def single_load(path_or_stream, ac_parser=None, ac_template=False,
                ac_context=None, **options):
    """
    Load single config file.

    :param path_or_stream: Configuration file path or file / file-like object
    :param ac_parser: Forced parser type or parser object
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: A dict presents context to instantiate template
    :param options: Optional keyword arguments such as:

        - Common options:

          - ac_namedtuple: Convert result to nested namedtuple object if True
          - ac_schema: JSON schema file path to validate given config file

        - Common backend options:

          - ignore_missing: Ignore and just return empty result if given file
            (``path_or_stream``) does not exist.

        - Backend specific options such as {"indent": 2} for JSON backend

    :return: dict or dict-like object supports merge operations
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

    schema = _load_schema(ac_template=ac_template, ac_context=ac_context,
                          **options)
    options["ac_schema"] = None  # It's not needed now.

    LOGGER.info("Loading: %s", filepath)
    if ac_template and filepath is not None:
        try:
            LOGGER.debug("Compiling: %s", filepath)
            content = anyconfig.template.render(filepath, ac_context)
            cnf = psr.loads(content, **options)
            return _maybe_validated(cnf, schema, **options)

        except Exception as exc:
            LOGGER.warning("Failed to compile %s, fallback to no template "
                           "mode, exc=%r", path_or_stream, exc)

    cnf = psr.load(path_or_stream, **options)
    return _maybe_validated(cnf, schema, **options)


def multi_load(paths, ac_parser=None, ac_template=False, ac_context=None,
               **options):
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
    :param options: Optional keyword arguments:

        - Common options:

          - ac_merge (merge): Specify strategy of how to merge results loaded
            from multiple configuration files. See the doc of :mod:`m9dicts`
            for more details of strategies. The default is m9dicts.MS_DICTS.

          - ac_marker (marker): Globbing marker to detect paths patterns.
          - ac_namedtuple: Convert result to nested namedtuple object if True
          - ac_schema: JSON schema file path to validate given config file

        - Common backend options:

          - ignore_missing: Ignore and just return empty result if given file
            (``path_or_stream``) does not exist.

        - Backend specific options such as {"indent": 2} for JSON backend

    :return: dict or dict-like object supports merge operations
    """
    marker = options.setdefault("ac_marker", options.get("marker", '*'))
    schema = _load_schema(ac_template=ac_template, ac_context=ac_context,
                          **options)
    options["ac_schema"] = None  # It's not needed now.

    cnf = to_container(ac_context, **options)
    same_type = anyconfig.utils.are_same_file_types(paths)

    if is_path(paths) and marker in paths:
        paths = anyconfig.utils.sglob(paths)

    for path in paths:
        opts = options.copy()
        opts["ac_namedtuple"] = False  # Disabled within this loop.
        # Nested patterns like ['*.yml', '/a/b/c.yml'].
        if is_path(path) and marker in path:
            cups = multi_load(path, ac_parser=ac_parser,
                              ac_template=ac_template, ac_context=cnf, **opts)
        else:
            if same_type:
                ac_parser = find_loader(path, ac_parser, is_path(path))
            cups = single_load(path, ac_parser=ac_parser,
                               ac_template=ac_template, ac_context=cnf, **opts)

        if cups:
            cnf.update(cups)

    return _maybe_validated(cnf, schema, **options)


def load(path_specs, ac_parser=None, ac_template=False, ac_context=None,
         **options):
    r"""
    Load single or multiple config files or multiple config files specified in
    given paths pattern.

    :param path_specs: Configuration file path or paths or its pattern such as
        r'/a/b/\*.json' or a list of files/file-like objects
    :param ac_parser: Forced parser type or parser object
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: A dict presents context to instantiate template
    :param options:
        Optional keyword arguments. See also the description of `options` in
        `multi_load` function.

    :return: dict or dict-like object supports merge operations
    """
    marker = options.setdefault("ac_marker", options.get("marker", '*'))

    if is_path(path_specs) and marker in path_specs or _is_paths(path_specs):
        return multi_load(path_specs, ac_parser=ac_parser,
                          ac_template=ac_template, ac_context=ac_context,
                          **options)
    else:
        return single_load(path_specs, ac_parser=ac_parser,
                           ac_template=ac_template, ac_context=ac_context,
                           **options)


def loads(content, ac_parser=None, ac_template=False, ac_context=None,
          **options):
    """
    :param content: Configuration file's content
    :param ac_parser: Forced parser type or parser object
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: Context dict to instantiate template
    :param options:
        Optional keyword arguments. See also the description of `options` in
        `single_load` function.

    :return: dict or dict-like object supports merge operations
    """
    msg = "Try parsing with a built-in parser because %s"
    if ac_parser is None:
        LOGGER.warning(msg, "ac_parser was not given.")
        return None

    psr = find_loader(None, ac_parser)
    if psr is None:
        LOGGER.warning(msg, "parser '%s' was not found" % ac_parser)
        return None

    schema = None
    ac_schema = options.get("ac_schema", None)
    if ac_schema is not None:
        options["ac_schema"] = None
        schema = loads(ac_schema, ac_parser=psr, ac_template=ac_template,
                       ac_context=ac_context, **options)

    if ac_template:
        try:
            LOGGER.debug("Compiling")
            content = anyconfig.template.render_s(content, ac_context)
        except Exception as exc:
            LOGGER.warning("Failed to compile and fallback to no template "
                           "mode: '%s', exc=%r", content[:50] + '...', exc)

    cnf = psr.loads(content, **options)
    return _maybe_validated(cnf, schema, **options)


def _find_dumper(path_or_stream, ac_parser=None):
    """
    Find configuration parser to dump data.

    :param path_or_stream: Output file path or file / file-like object
    :param ac_parser: Forced parser type or parser object

    :return: Parser-inherited class object
    """
    psr = find_loader(path_or_stream, ac_parser)

    if psr is None or not getattr(psr, "dump", False):
        LOGGER.warning("Dump method not implemented. Fallback to json.Parser")
        psr = anyconfig.backend.json.Parser()

    return psr


def dump(data, path_or_stream, ac_parser=None, **options):
    """
    Save `data` as `path_or_stream`.

    :param data: Config data object (dict[-like] or namedtuple) to dump
    :param path_or_stream: Output file path or file / file-like object
    :param ac_parser: Forced parser type or parser object
    :param options:
        Backend specific optional arguments, e.g. {"indent": 2} for JSON
        loader/dumper backend
    """
    dumper = _find_dumper(path_or_stream, ac_parser)
    LOGGER.info("Dumping: %s",
                anyconfig.utils.get_path_from_stream(path_or_stream))
    if anyconfig.mdicts.is_namedtuple(data):
        data = to_container(data, **options)  # namedtuple -> dict-like
    dumper.dump(data, path_or_stream, **options)


def dumps(data, ac_parser=None, **options):
    """
    Return string representation of `data` in forced type format.

    :param data: Config data object to dump
    :param ac_parser: Forced parser type or parser object
    :param options: see :func:`dump`

    :return: Backend-specific string representation for the given data
    """
    if anyconfig.mdicts.is_namedtuple(data):
        data = to_container(data, **options)
    return _find_dumper(None, ac_parser).dumps(data, **options)

# vim:sw=4:ts=4:et:
