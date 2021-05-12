#
# Copyright (C) 2012 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=unused-import,import-error,invalid-name
r"""Public APIs of anyconfig module to load configuration files.
"""
import typing
import warnings

from ..common import (
    InDataT, InDataExT, PathOrIOInfoT
)
from ..dicts import (
    convert_to as dicts_convert_to,
    merge as dicts_merge
)
from ..ioinfo import make as ioinfo_make
from ..parsers import find as parsers_find
from ..query import try_query
from ..schema import is_valid
from ..template import try_render
from ..utils import (
    are_same_file_types, expand_paths,
    is_dict_like, is_path_like_object, is_paths
)
from .datatypes import (
    ParserT
)


MappingT = typing.Dict[str, typing.Any]
MaybeParserOrIdOrTypeT = typing.Optional[typing.Union[str, ParserT]]


def _maybe_schema(**options) -> typing.Optional[InDataT]:
    """
    :param options: Optional keyword arguments such as

        - ac_template: Assume configuration file may be a template file and try
          to compile it AAR if True
        - ac_context: Mapping object presents context to instantiate template
        - ac_schema: JSON schema file path to validate configuration files

    :return: Mapping object or None means some errors
    """
    ac_schema = options.get("ac_schema", None)
    if ac_schema is not None:
        # Try to detect the appropriate parser to load the schema data as it
        # may be different from the original config file's format, perhaps.
        options["ac_parser"] = None
        options["ac_schema"] = None  # Avoid infinite loop.
        return load(ac_schema, **options)

    return None


def _single_load(input_: PathOrIOInfoT,
                 ac_parser: MaybeParserOrIdOrTypeT = None,
                 ac_template: typing.Optional[PathOrIOInfoT] = None,
                 ac_context: typing.Optional[MappingT] = None,
                 **options) -> InDataExT:
    """
    :param input_:
        File path or file or file-like object or pathlib.Path object represents
        the file or a namedtuple 'anyconfig.common.IOInfo' object represents
        some input to load some data from
    :param ac_parser: Forced parser type or parser object itself
    :param ac_template:
        Assume configuration file may be a template file and try to compile it
        AAR if True
    :param ac_context: A dict presents context to instantiate template
    :param options:
        Optional keyword arguments :func:`single_load` supports except for
        ac_schema and ac_query

    :return: Mapping object
    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    ioi = ioinfo_make(input_)
    psr: ParserT = parsers_find(ioi, forced_type=ac_parser)
    filepath = ioi.path

    # .. note::
    #    This will be kept for backward compatibility until 'ignore_missing'
    #    option is deprecated and removed completely.
    if "ignore_missing" in options:
        warnings.warn("keyword option 'ignore_missing' is deprecated, use "
                      "'ac_ignore_missing' instead", DeprecationWarning)
        options["ac_ignore_missing"] = options["ignore_missing"]

    if ac_template is not None and filepath is not None:
        content = try_render(filepath=filepath, ctx=ac_context, **options)
        if content is not None:
            return psr.loads(content, **options)

    return psr.load(ioi, **options)


def single_load(input_: PathOrIOInfoT,
                ac_parser: MaybeParserOrIdOrTypeT = None,
                ac_template: typing.Optional[PathOrIOInfoT] = None,
                ac_context: typing.Optional[MappingT] = None,
                **options) -> InDataExT:
    r"""
    Load single configuration file.

    .. note::

       :func:`load` is a preferable alternative and this API should be used
       only if there is a need to emphasize given input 'input\_' is single
       one.

    :param input\_:
        File path or file or file-like object or pathlib.Path object represents
        the file or a namedtuple 'anyconfig.common.IOInfo' object represents
        some input to load some data from
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
            this option was not given or None, dict or
            :class:`collections.OrderedDict` will be used to make result as
            mapping object depends on if ac_ordered (see below) is True and
            selected backend can keep the order of items loaded. See also
            :meth:`_container_factory` of
            :class:`anyconfig.backend.base.Parser` for more implementation
            details.

          - ac_ordered: True if you want to keep resuls ordered. Please note
            that order of items may be lost depends on the selected backend.

          - ac_schema: JSON schema file path to validate given config file
          - ac_query: JMESPath expression to query data

        - Common backend options:

          - ac_ignore_missing:
            Ignore and just return empty result if given file 'input\_' does
            not exist actually.

        - Backend specific options such as {"indent": 2} for JSON backend

    :return: Mapping object
    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    cnf = _single_load(input_, ac_parser=ac_parser, ac_template=ac_template,
                       ac_context=ac_context, **options)
    schema = _maybe_schema(ac_template=ac_template, ac_context=ac_context,
                           **options)
    if schema and not is_valid(cnf, schema, **options):
        return None

    return try_query(cnf, options.get('ac_query', False), **options)


def multi_load(inputs: typing.Union[typing.Iterable[PathOrIOInfoT],
                                    PathOrIOInfoT],
               ac_parser: MaybeParserOrIdOrTypeT = None,
               ac_template: typing.Optional[PathOrIOInfoT] = None,
               ac_context: typing.Optional[MappingT] = None,
               **options) -> InDataExT:
    r"""
    Load multiple config files.

    .. note::

       :func:`load` is a preferable alternative and this API should be used
       only if there is a need to emphasize given inputs are multiple ones.

    The first argument 'inputs' may be a list of a file paths or a glob pattern
    specifying them or a pathlib.Path object represents file[s] or a namedtuple
    'anyconfig.common.IOInfo' object represents some inputs to load some data
    from.

    About glob patterns, for example, is, if a.yml, b.yml and c.yml are in the
    dir /etc/foo/conf.d/, the followings give same results::

      multi_load(["/etc/foo/conf.d/a.yml", "/etc/foo/conf.d/b.yml",
                  "/etc/foo/conf.d/c.yml", ])

      multi_load("/etc/foo/conf.d/*.yml")

    :param inputs:
        A list of file path or a glob pattern such as r'/a/b/\*.json'to list of
        files, file or file-like object or pathlib.Path object represents the
        file or a namedtuple 'anyconfig.common.IOInfo' object represents some
        inputs to load some data from
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
            :mod:`dicts` for more details of strategies. The default
            is dicts.MS_DICTS.

          - ac_marker (marker): Globbing marker to detect paths patterns.

        - Common backend options:

          - ignore_missing: Ignore and just return empty result if given file
            'path' does not exist.

        - Backend specific options such as {"indent": 2} for JSON backend

    :return: Mapping object or any query result might be primitive objects
    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    marker = options.setdefault("ac_marker", options.get("marker", '*'))
    schema = _maybe_schema(ac_template=ac_template, ac_context=ac_context,
                           **options)
    options["ac_schema"] = None  # Avoid to load schema more than twice.

    paths = [ioinfo_make(p) for p in expand_paths(inputs, marker=marker)]
    if are_same_file_types(paths):
        ac_parser = parsers_find(paths[0], forced_type=ac_parser)

    cnf = ac_context
    for path in paths:
        opts = options.copy()
        cups = _single_load(path, ac_parser=ac_parser,
                            ac_template=ac_template, ac_context=cnf, **opts)
        if cups:
            if cnf is None:
                cnf = cups  # type: ignore
            elif is_dict_like(cups):
                dicts_merge(cnf, typing.cast(MappingT, cups), **options)

    if cnf is None:
        return dicts_convert_to({}, **options)

    if schema and not is_valid(cnf, schema, **options):
        return None

    return try_query(cnf, options.get('ac_query', False), **options)


def load(path_specs, ac_parser=None, ac_dict=None, ac_template=False,
         ac_context=None, **options):
    r"""
    Load single or multiple config files or multiple config files specified in
    given paths pattern or pathlib.Path object represents config files or a
    namedtuple 'anyconfig.common.IOInfo' object represents some inputs.

    :param path_specs:
        A list of file path or a glob pattern such as r'/a/b/\*.json'to list of
        files, file or file-like object or pathlib.Path object represents the
        file or a namedtuple 'anyconfig.common.IOInfo' object represents some
        inputs to load some data from.
    :param ac_parser: Forced parser type or parser object
    :param ac_dict:
        callable (function or class) to make mapping object will be returned as
        a result or None. If not given or ac_dict is None, default mapping
        object used to store resutls is dict or
        :class:`collections.OrderedDict` if ac_ordered is True and selected
        backend can keep the order of items in mapping objects.

    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: A dict presents context to instantiate template
    :param options:
        Optional keyword arguments. See also the description of 'options' in
        :func:`single_load` and :func:`multi_load`

    :return: Mapping object or any query result might be primitive objects
    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    marker = options.setdefault("ac_marker", options.get("marker", '*'))

    if is_path_like_object(path_specs, marker):
        return single_load(path_specs, ac_parser=ac_parser, ac_dict=ac_dict,
                           ac_template=ac_template, ac_context=ac_context,
                           **options)

    if not is_paths(path_specs, marker):
        raise ValueError("Possible invalid input %r" % path_specs)

    return multi_load(path_specs, ac_parser=ac_parser, ac_dict=ac_dict,
                      ac_template=ac_template, ac_context=ac_context,
                      **options)


def loads(content, ac_parser=None, ac_dict=None, ac_template=False,
          ac_context=None, **options):
    """
    :param content: Configuration file's content (a string)
    :param ac_parser: Forced parser type or ID or parser object
    :param ac_dict:
        callable (function or class) to make mapping object will be returned as
        a result or None. If not given or ac_dict is None, default mapping
        object used to store resutls is dict or
        :class:`collections.OrderedDict` if ac_ordered is True and selected
        backend can keep the order of items in mapping objects.
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: Context dict to instantiate template
    :param options:
        Optional keyword arguments. See also the description of 'options' in
        :func:`single_load` function.

    :return: Mapping object or any query result might be primitive objects
    :raises: ValueError, UnknownProcessorTypeError
    """
    if ac_parser is None:
        warnings.warn("ac_parser was not given but it's must to find correct "
                      "parser to load configurations from string.")
        return None

    psr = parsers_find(None, forced_type=ac_parser)
    schema = None
    ac_schema = options.get("ac_schema", None)
    if ac_schema is not None:
        options["ac_schema"] = None
        schema = loads(ac_schema, ac_parser=psr, ac_dict=ac_dict,
                       ac_template=ac_template, ac_context=ac_context,
                       **options)

    if ac_template:
        compiled = try_render(content=content, ctx=ac_context, **options)
        if compiled is not None:
            content = compiled

    cnf = psr.loads(content, ac_dict=ac_dict, **options)
    if not is_valid(cnf, schema, **options):
        return None

    return try_query(cnf, options.get('ac_query', False), **options)

# vim:sw=4:ts=4:et:
