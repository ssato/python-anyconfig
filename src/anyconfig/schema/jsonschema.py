#
# Copyright (C) 2015 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Implementation using jsonschema provides the following functions.

- validate(data: typing.Dict[str, typing.Any],
           schema: typing.Dict[str, typing.Any],
           ac_schema_safe: bool = True, ac_schema_errors: bool = False,
           **options) -> typing.Tuple[bool, str]:
  validate with schema

- gen_schema(data: typing.Dict[str, typing.Any],
             **options) -> typing.Dict[str, typing.Any]:
  Generate an object represents a schema
"""
import typing
import warnings

import jsonschema

from ..common import (
    ValidationError, InDataExT, InDataT
)
from ..utils import (
    filter_options, is_dict_like, is_list_like
)
from .datatypes import ResultT


def _validate_all(data: InDataExT, schema: InDataT, **_options) -> ResultT:
    """Do all of the validation checks.

    See the description of :func:`validate` for more details of parameters and
    return value.

    :seealso: https://python-jsonschema.readthedocs.io/en/latest/validate/,
    a section of 'iter_errors' especially
    """
    vldtr = jsonschema.Draft7Validator(schema)  # :raises: SchemaError, ...
    errors = list(vldtr.iter_errors(data))

    return (not errors, [err.message for err in errors])


def _validate(data: InDataExT, schema: InDataT, ac_schema_safe: bool = True,
              **options: typing.Any) -> ResultT:
    """Validate ``data`` with ``schema``.

    See the description of :func:`validate` for more details of parameters and
    return value.

    Validate target object 'data' with given schema object.
    """
    try:
        jsonschema.validate(
            data, schema, format_checker=jsonschema.draft7_format_checker,
            **options
        )
    except (jsonschema.ValidationError, jsonschema.SchemaError,
            Exception) as exc:
        if ac_schema_safe:
            return (False, str(exc))  # Validation was failed.
        raise

    return (True, '')


def validate(data: InDataExT, schema: InDataT, ac_schema_safe: bool = True,
             ac_schema_errors: bool = False, **options: typing.Any
             ) -> ResultT:
    """Validate target object with given schema object.

    See also: https://python-jsonschema.readthedocs.org/en/latest/validate/

    :parae data: Target object (a dict or a dict-like object) to validate
    :param schema: Schema object (a dict or a dict-like object)
        instantiated from schema JSON file or schema JSON string
    :param options: Other keyword options such as:

        - ac_schema_safe: Exception (jsonschema.ValidationError or
          jsonschema.SchemaError or others) will be thrown during validation
          process due to any validation or related errors. However, these will
          be catched by default, and will be re-raised if this value is False.

        - ac_schema_errors: Lazily yield each of the validation errors and
          returns all of them if validation fails.

    :return: (True if validation succeeded else False, error message[s])
    """
    options = filter_options(('cls', ), options)
    if ac_schema_errors:
        return _validate_all(data, schema, **options)

    return _validate(data, schema, ac_schema_safe, **options)


def is_valid(data: InDataExT, schema: InDataT, ac_schema_safe: bool = True,
             ac_schema_errors: bool = False, **options) -> bool:
    """Raise ValidationError if ``data`` was invalidated by schema `schema`."""
    if schema is None or not schema:
        return True

    (_success, error_or_errors) = validate(
        data, schema, ac_schema_safe=True,
        ac_schema_errors=ac_schema_errors, **options
    )
    if error_or_errors:
        msg = f'scm={schema!s}, err={error_or_errors!s}'
        if ac_schema_safe:
            warnings.warn(msg)
            return False

        raise ValidationError(msg)

    return True


_SIMPLETYPE_MAP: typing.Dict[typing.Any, str] = {
    list: 'array', tuple: 'array', bool: 'boolean', int: 'integer', float:
    'number', dict: 'object', str: 'string'
}


def _process_options(**options):
    """Help to process keyword arguments passed to gen_schema.

    :return: A tuple of (typemap :: dict, strict :: bool)
    """
    return (options.get('ac_schema_typemap', _SIMPLETYPE_MAP),
            bool(options.get('ac_schema_strict', False)))


def array_to_schema(iarr: typing.Iterable[InDataT], **options
                    ) -> typing.Dict[str, typing.Any]:
    """Generate a JSON schema object with type annotation added for ``iaa```.

    :param arr: Array of mapping objects like dicts
    :param options: Other keyword options such as:

        - ac_schema_strict: True if more strict (precise) schema is needed
        - ac_schema_typemap: Type to JSON schema type mappings

    :return: Another mapping objects represents JSON schema of items
    """
    (typemap, strict) = _process_options(**options)

    arr: typing.List[InDataT] = list(iarr)
    scm = {
        'type': typemap[list],
        'items': gen_schema(arr[0] if arr else 'str', **options)
    }
    if strict:
        nitems = len(arr)
        scm['minItems'] = nitems
        scm['uniqueItems'] = len(set(arr)) == nitems

    return scm


def object_to_schema(obj: InDataT, **options) -> InDataT:
    """Generate a node represents JSON schema object for ``obj``.

    Type annotation will be added for given object node at the same time.

    :param obj: mapping object such like a dict
    :param options: Other keyword options such as:

        - ac_schema_strict: True if more strict (precise) schema is needed
        - ac_schema_typemap: Type to JSON schema type mappings

    :yield: Another mapping objects represents JSON schema of object
    """
    (typemap, strict) = _process_options(**options)

    props = dict((k, gen_schema(v, **options)) for k, v in obj.items())
    scm = {'type': typemap[dict], 'properties': props}
    if strict:
        scm['required'] = sorted(props.keys())

    return scm


_SIMPLE_TYPES = (bool, int, float, str)


def gen_schema(data: InDataExT, **options) -> InDataT:
    """Generate a JSON schema object validates ``data``.

    :param data: Configuration data object (dict[-like] or namedtuple)
    :param options: Other keyword options such as:

        - ac_schema_strict: True if more strict (precise) schema is needed
        - ac_schema_typemap: Type to JSON schema type mappings

    :return: A dict represents JSON schema of this node
    """
    if data is None:
        return {'type': 'null'}

    _type = type(data)

    if _type in _SIMPLE_TYPES:
        typemap = options.get('ac_schema_typemap', _SIMPLETYPE_MAP)
        scm = {'type': typemap[_type]}

    elif is_dict_like(data):
        scm = object_to_schema(data, **options)  # type: ignore

    elif is_list_like(data):
        scm = array_to_schema(
            typing.cast(typing.Iterable[InDataT], data), **options
        )

    return scm

# vim:sw=4:ts=4:et:
