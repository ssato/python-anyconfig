#
# Copyright (C) 2015, 2016 Satoru SATOH <ssato redhat.com>
# License: MIT
#
"""anyconfig.schema module.

.. versionchanged:: 0.7.0
   allow passing `ac_schema_strict` to API :func:`gen_schema` to generate more
   strict and precise JSON schema object

.. versionadded:: 0.0.11
   Added new API :func:`gen_schema` to generate schema object

.. versionadded:: 0.0.10
   Added new API :func:`validate` to validate config with JSON schema
"""
from __future__ import absolute_import
try:
    import jsonschema
except ImportError:
    pass

import anyconfig.compat


_SIMPLETYPE_MAP = {list: "array", tuple: "array",
                   bool: "boolean",
                   int: "integer", float: "number",
                   dict: "object",
                   str: "string"}
_SIMPLE_TYPES = (bool, int, float, str)

if not anyconfig.compat.IS_PYTHON_3:
    try:
        _SIMPLETYPE_MAP[unicode] = "string"
        _SIMPLE_TYPES = (bool, int, float, str, unicode)
    except NameError:
        pass


def validate(obj, schema, **options):
    """
    Validate target object with given schema object, loaded from JSON schema.

    See also: https://python-jsonschema.readthedocs.org/en/latest/validate/

    :parae obj: Target object (a dict or a dict-like object) to validate
    :param schema: Schema object (a dict or a dict-like object)
        instantiated from schema JSON file or schema JSON string
    :param options: Other keyword options such as:

        - format_checker: A format property checker object of which class is
          inherited from jsonschema.FormatChecker, it's default if None given.

        - safe: Exception (jsonschema.ValidationError or jsonschema.SchemaError
          or others) will be thrown during validation process due to any
          validation or related errors. However, these will be catched by
          default, and will be re-raised if `safe` is False.

    :return: (True if validation succeeded else False, error message)
    """
    format_checker = options.get("format_checker", None)
    try:
        if format_checker is None:
            format_checker = jsonschema.FormatChecker()  # :raises: NameError
        try:
            jsonschema.validate(obj, schema, format_checker=format_checker)
            return (True, '')
        except (jsonschema.ValidationError, jsonschema.SchemaError,
                Exception) as exc:
            if options.get("safe", True):
                return (False, str(exc))
            else:
                raise

    except NameError:
        return (True, "Validation module (jsonschema) is not available")

    return (True, '')


def _process_options(**options):
    """
    Helper function to process keyword arguments passed to gen_schema.

    :return: A tuple of (typemap :: dict, strict :: bool)
    """
    return (options.get("ac_schema_typemap", _SIMPLETYPE_MAP),
            bool(options.get("ac_schema_strict", False)))


def array_to_schema(arr, **options):
    """
    Generate a JSON schema object with type annotation added for given object.

    :param arr: Array of dict or MergeableDict objects
    :param options: Other keyword options such as:

        - ac_schema_strict: True if more strict (precise) schema is needed
        - ac_schema_typemap: Type to JSON schema type mappings

    :return: Another MergeableDict instance represents JSON schema of items
    """
    (typemap, strict) = _process_options(**options)

    arr = list(arr)
    scm = dict(type=typemap[list],
               items=gen_schema(arr[0] if arr else "str", **options))
    if strict:
        nitems = len(arr)
        scm["minItems"] = nitems
        scm["uniqueItems"] = len(set(arr)) == nitems

    return scm


def object_to_schema(obj, **options):
    """
    Generate a node represents JSON schema object with type annotation added
    for given object node.

    :param obj: Dict or MergeableDict object
    :param options: Other keyword options such as:

        - ac_schema_strict: True if more strict (precise) schema is needed
        - ac_schema_typemap: Type to JSON schema type mappings

    :yield: Another MergeableDict instance represents JSON schema of object
    """
    (typemap, strict) = _process_options(**options)

    props = dict((k, gen_schema(v, **options)) for k, v in obj.items())
    scm = dict(type=typemap[dict], properties=props)
    if strict:
        scm["required"] = sorted(props.keys())

    return scm


def gen_schema(node, **options):
    """
    Generate a node represents JSON schema object with type annotation added
    for given object node.

    :param node: Config data object (dict[-like] or namedtuple)
    :param options: Other keyword options such as:

        - ac_schema_strict: True if more strict (precise) schema is needed
        - ac_schema_typemap: Type to JSON schema type mappings

    :return: A dict represents JSON schema of this node
    """
    if node is None:
        return dict(type="null")

    _type = type(node)

    if _type in _SIMPLE_TYPES:
        typemap = options.get("ac_schema_typemap", _SIMPLETYPE_MAP)
        scm = dict(type=typemap[_type])

    elif isinstance(node, dict):
        scm = object_to_schema(node, **options)

    elif _type in (list, tuple) or hasattr(node, "__iter__"):
        scm = array_to_schema(node, **options)

    return scm

# vim:sw=4:ts=4:et:
