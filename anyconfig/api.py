#
# Copyright (C) 2012 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=unused-import,import-error,invalid-name
r"""Public APIs of anyconfig module.

.. versionadded:: 0.8.3

   - Added ac_dict keyword option to pass dict factory (any callable like
     function or class) to make dict-like object in backend parsers.
   - Added ac_query keyword option to query data with JMESPath expression.
   - Added experimental query api to query data with JMESPath expression.
   - Removed ac_namedtuple keyword option.
   - Export :func:`merge`.
   - Stop exporting :func:`to_container` which was deprecated and removed.

.. versionadded:: 0.8.2

   - Added new API, version to provide version information.

.. versionadded:: 0.8.0

   - Removed set_loglevel API as it does not help much.
   - Added :func:`open` API to open files with appropriate open mode.
   - Added custom exception classes, :class:`UnknownParserTypeError` and
     :class:`UnknownFileTypeError` to express specific errors.
   - Change behavior of the API :func:`find_loader` and others to make them
     fail firt and raise exceptions (ValueError, UnknownParserTypeError or
     UnknownFileTypeError) as much as possible if wrong parser type for uknown
     file type was given.

.. versionadded:: 0.5.0

   - Most keyword arguments passed to APIs are now position independent.
   - Added ac_namedtuple parameter to \*load and \*dump APIs.

.. versionchanged:: 0.3

   - Replaced `forced_type` optional argument of some public APIs with
     `ac_parser` to allow skip of config parser search by passing parser object
     previously found and instantiated.

     Also removed some optional arguments, `ignore_missing`, `merge` and
     `marker`, from definitions of some public APIs as these may not be changed
     from default in common use cases.

.. versionchanged:: 0.2

   - Now APIs :func:`find_loader`, :func:`single_load`, :func:`multi_load`,
     :func:`load` and :func:`dump` can process a file/file-like object or a
     list of file/file-like objects instead of a file path or a list of file
     paths.

.. versionadded:: 0.2

   - Export factory method (create) of anyconfig.mergeabledict.MergeableDict
"""
from __future__ import absolute_import

import os.path

from anyconfig.globals import LOGGER
import anyconfig.backends
import anyconfig.backend.json
import anyconfig.compat
import anyconfig.query
import anyconfig.globals
import anyconfig.dicts
import anyconfig.template
import anyconfig.utils

# Import some global constants will be re-exported:
from anyconfig.backends import (
    UnknownParserTypeError, UnknownFileTypeError
)
from anyconfig.dicts import (
    MS_REPLACE, MS_NO_REPLACE, MS_DICTS, MS_DICTS_AND_LISTS, MERGE_STRATEGIES,
    get, set_, merge # flake8: noqa
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


def _maybe_validated(cnf, schema, **options):
    """
    :param cnf: Mapping object represents configuration data
    :param schema: JSON schema object
    :param options: Keyword options passed to :func:`~jsonschema.validate`

    :return: Given `cnf` as it is if validation succeeds else None
    """
    valid = True
    if schema:
        (valid, msg) = validate(cnf, schema, safe=True, **options)
        if msg:
            LOGGER.warning(msg)

    if valid:
        return cnf

    return None


def version():
    """
    :return: A tuple of version info, (major, minor, release), e.g. (0, 8, 2)
    """
    return anyconfig.globals.VERSION.split('.')


def find_loader(path_or_stream, parser_or_type=None, is_path_=False):
    """
    Find out parser object appropriate to load configuration from a file of
    given path or file or file-like object.

    :param path_or_stream: Configuration file path or file or file-like object
    :param parser_or_type:
        Forced configuration parser type or parser object itself
    :param is_path_: Specify True if given `path_or_stream` is a file path

    :return:
        An instance of a class inherits :class:`~anyconfig.backend.base.Parser`
        or None
    """
    if anyconfig.backends.is_parser(parser_or_type):
        return parser_or_type

    try:
        psr = anyconfig.backends.find_parser(path_or_stream,
                                             forced_type=parser_or_type,
                                             is_path_=is_path_)
        LOGGER.debug("Using config parser: %r [%s]", psr, psr.type())
        return psr()  # TBD: Passing initialization arguments.
    except (ValueError, UnknownParserTypeError, UnknownFileTypeError):
        raise


def _maybe_schema(**options):
    """
    :param options: Optional keyword arguments such as

        - ac_template: Assume configuration file may be a template file and try
          to compile it AAR if True
        - ac_context: Mapping object presents context to instantiate template
        - ac_schema: JSON schema file path to validate configuration files
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


# pylint: disable=redefined-builtin
def open(path, mode=None, ac_parser=None, **options):
    """
    Open given configuration file with appropriate open flag.

    :param path: Configuration file path
    :param mode:
        Can be 'r' and 'rb' for reading (default) or 'w', 'wb' for writing.
        Please note that even if you specify 'r' or 'w', it will be changed to
        'rb' or 'wb' if selected backend, xml and configobj for example, for
        given config file prefer that.
    :param options:
        Optional keyword arguments passed to the internal file opening APIs of
        each backends such like 'buffering' optional parameter passed to
        builtin 'open' function.

    :return: A file object or None on any errors
    """
    psr = find_loader(path, parser_or_type=ac_parser, is_path_=True)
    if mode is not None and mode.startswith('w'):
        return psr.wopen(path, **options)

    return psr.ropen(path, **options)


def single_load(path_or_stream, ac_parser=None, ac_template=False,
                ac_context=None, **options):
    """
    Load single configuration file.

    .. note::

       :func:`load` is a preferable alternative and this API should be used
       only if there is a need to emphasize given file path is single one.

    :param path_or_stream: Configuration file path or file or file-like object
    :param ac_parser: Forced parser type or parser object itself
    :param ac_template:
        Assume configuration file may be a template file and try to compile it
        AAR if True
    :param ac_context: A dict presents context to instantiate template
    :param options: Optional keyword arguments such as:

        - Options common in :func:`single_load`, :func:`multi_load`,
          :func:`load` and :func:`loads`:

          - ac_dict: callable (function or class) to make mapping objects from
            loaded data if the selected backend can customize that such as JSON
            which supports that with 'object_pairs_hook' option, or None. If
            this option was not given or None, dict or :class:`OrderedDict`
            will be used to make result as mapping object depends on if
            ac_ordered (see below) is True and selected backend can keep the
            order of items loaded. See also :meth:`_container_factory` of
            :class:`~anyconfig.backend.base.Parser` for more implementation
            details.

          - ac_ordered: True if you want to keep resuls ordered. Please note
            that order of items may be lost depends on the selected backend.

          - ac_schema: JSON schema file path to validate given config file
          - ac_query: JMESPath expression to query data

        - Common backend options:

          - ignore_missing: Ignore and just return empty result if given file
            (``path_or_stream``) does not exist.

        - Backend specific options such as {"indent": 2} for JSON backend

    :return: Mapping object
    """
    is_path_ = is_path(path_or_stream)
    if is_path_:
        filepath = path_or_stream = anyconfig.utils.normpath(path_or_stream)
    else:
        filepath = anyconfig.utils.get_path_from_stream(path_or_stream)

    psr = find_loader(path_or_stream, ac_parser, is_path_)
    schema = _maybe_schema(ac_template=ac_template, ac_context=ac_context,
                           **options)

    LOGGER.info("Loading: %s", filepath)
    if ac_template and filepath is not None:
        content = anyconfig.template.try_render(filepath=filepath,
                                                ctx=ac_context)
        if content is not None:
            cnf = psr.loads(content, **options)
            return _maybe_validated(cnf, schema, **options)

    cnf = psr.load(path_or_stream, **options)
    return _maybe_validated(cnf, schema, **options)


def multi_load(paths, ac_parser=None, ac_template=False, ac_context=None,
               **options):
    """
    Load multiple config files.

    .. note::

       :func:`load` is a preferable alternative and this API should be used
       only if there is a need to emphasize given file paths are multiple ones.

    The first argument `paths` may be a list of config file paths or
    a glob pattern specifying that. That is, if a.yml, b.yml and c.yml are in
    the dir /etc/foo/conf.d/, the followings give same results::

      multi_load(["/etc/foo/conf.d/a.yml", "/etc/foo/conf.d/b.yml",
                  "/etc/foo/conf.d/c.yml", ])

      multi_load("/etc/foo/conf.d/*.yml")

    :param paths:
        List of configuration file paths or a glob pattern to list of these
        paths, or a list of file or file-like objects
    :param ac_parser: Forced parser type or parser object
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: Mapping object presents context to instantiate template
    :param options: Optional keyword arguments:

        - ac_dict, ac_ordered, ac_schema and ac_query are the options common in
          :func:`single_load`, :func:`multi_load`, :func:`load`: and
          :func:`loads`. See the descriptions of them in :func:`single_load`.

        - Options specific to this function and :func:`load`:

          - ac_merge (merge): Specify strategy of how to merge results loaded
            from multiple configuration files. See the doc of
            :mod:`anyconfig.dicts` for more details of strategies. The default
            is anyconfig.dicts.MS_DICTS.

          - ac_marker (marker): Globbing marker to detect paths patterns.

        - Common backend options:

          - ignore_missing: Ignore and just return empty result if given file
            (``path_or_stream``) does not exist.

        - Backend specific options such as {"indent": 2} for JSON backend

    :return: Mapping object or any query result might be primitive objects
    """
    marker = options.setdefault("ac_marker", options.get("marker", '*'))
    schema = _maybe_schema(ac_template=ac_template, ac_context=ac_context,
                           **options)
    options["ac_schema"] = None  # Avoid to load schema more than twice.

    paths = anyconfig.utils.norm_paths(paths, marker=marker)
    if anyconfig.utils.are_same_file_types(paths):
        ac_parser = find_loader(paths[0], ac_parser, is_path(paths[0]))

    cnf = ac_context
    for path in paths:
        opts = options.copy()
        cups = single_load(path, ac_parser=ac_parser,
                           ac_template=ac_template, ac_context=cnf, **opts)
        if cups:
            if cnf is None:
                cnf = cups
            else:
                merge(cnf, cups, **options)

    if cnf is None:
        return anyconfig.dicts.convert_to({}, **options)

    cnf = _maybe_validated(cnf, schema, **options)
    return anyconfig.query.query(cnf, **options)


def load(path_specs, ac_parser=None, ac_dict=None, ac_template=False,
         ac_context=None, **options):
    r"""
    Load single or multiple config files or multiple config files specified in
    given paths pattern.

    :param path_specs: Configuration file path or paths or its pattern such as
        r'/a/b/\*.json' or a list of files/file-like objects
    :param ac_parser: Forced parser type or parser object
    :param ac_dict:
        callable (function or class) to make mapping object will be returned as
        a result or None. If not given or ac_dict is None, default mapping
        object used to store resutls is dict or
        :class:`~collections.OrderedDict` if ac_ordered is True and selected
        backend can keep the order of items in mapping objects.

    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: A dict presents context to instantiate template
    :param options:
        Optional keyword arguments. See also the description of `options` in
        :func:`single_load` and :func:`multi_load`

    :return: Mapping object or any query result might be primitive objects
    """
    marker = options.setdefault("ac_marker", options.get("marker", '*'))

    if is_path(path_specs) and marker in path_specs or _is_paths(path_specs):
        return multi_load(path_specs, ac_parser=ac_parser, ac_dict=ac_dict,
                          ac_template=ac_template, ac_context=ac_context,
                          **options)
    else:
        cnf = single_load(path_specs, ac_parser=ac_parser, ac_dict=ac_dict,
                          ac_template=ac_template, ac_context=ac_context,
                          **options)
        return anyconfig.query.query(cnf, **options)


def loads(content, ac_parser=None, ac_dict=None, ac_template=False,
          ac_context=None, **options):
    """
    :param content: Configuration file's content
    :param ac_parser: Forced parser type or parser object
    :param ac_dict:
        callable (function or class) to make mapping object will be returned as
        a result or None. If not given or ac_dict is None, default mapping
        object used to store resutls is dict or
        :class:`~collections.OrderedDict` if ac_ordered is True and selected
        backend can keep the order of items in mapping objects.
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: Context dict to instantiate template
    :param options:
        Optional keyword arguments. See also the description of `options` in
        :func:`single_load` function.

    :return: Mapping object or any query result might be primitive objects
    """
    if ac_parser is None:
        LOGGER.warning("ac_parser was not given but it's must to find correct "
                       "parser to load configurations from string.")
        return None

    psr = find_loader(None, ac_parser)
    schema = None
    ac_schema = options.get("ac_schema", None)
    if ac_schema is not None:
        options["ac_schema"] = None
        schema = loads(ac_schema, ac_parser=psr, ac_dict=ac_dict,
                       ac_template=ac_template, ac_context=ac_context,
                       **options)

    if ac_template:
        compiled = anyconfig.template.try_render(content=content,
                                                 ctx=ac_context)
        if compiled is not None:
            content = compiled

    cnf = psr.loads(content, ac_dict=ac_dict, **options)
    cnf = _maybe_validated(cnf, schema, **options)
    return anyconfig.query.query(cnf, **options)


def _find_dumper(path_or_stream, ac_parser=None):
    """
    Find parser to dump configuration data.

    :param path_or_stream: Output file path or file / file-like object
    :param ac_parser: Forced parser type or parser object

    :return: Parser object
    """
    return find_loader(path_or_stream, ac_parser)


def dump(data, path_or_stream, ac_parser=None, **options):
    """
    Save `data` as `path_or_stream`.

    :param data: A mapping object may have configurations data to dump
    :param path_or_stream: Output file path or file / file-like object
    :param ac_parser: Forced parser type or parser object
    :param options:
        Backend specific optional arguments, e.g. {"indent": 2} for JSON
        loader/dumper backend
    """
    dumper = _find_dumper(path_or_stream, ac_parser)
    LOGGER.info("Dumping: %s",
                anyconfig.utils.get_path_from_stream(path_or_stream))
    dumper.dump(data, path_or_stream, **options)


def dumps(data, ac_parser=None, **options):
    """
    Return string representation of `data` in forced type format.

    :param data: Config data object to dump
    :param ac_parser: Forced parser type or parser object
    :param options: see :func:`dump`

    :return: Backend-specific string representation for the given data
    """
    return _find_dumper(None, ac_parser).dumps(data, **options)


def query(data, expression, **options):
    """
    API just wraps :func:`anyconfig.query.query`.

    :param data: Config data object to query
    :param options: Ignored in current implementation

    :return: Query result object may be primitive (int, str, etc.) or dict.
    """
    return anyconfig.query.query(data, ac_query=expression)

# vim:sw=4:ts=4:et:
