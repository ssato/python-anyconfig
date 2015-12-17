#
# Copyright (C) 2015 Satoru SATOH <ssato redhat.com>
# License: MIT
#
"""anyconfig.schema module.

.. versionadded:: 0.0.11
   Added new API :func:`gen_schema` to generate schema object

.. versionadded:: 0.0.10
   Added new API :func:`validate` to validate config with JSON schema
"""
from __future__ import absolute_import
import anyconfig.compat

try:
    import jsonschema
except ImportError:
    pass


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


def array_to_schema_node(arr, typemap=None):
    """
    Generate a node represents JSON schema object with type annotation added
    for given object node.

    :param arr: Array of dict or MergeableDict objects
    :param typemap: Type to JSON schema type mappings

    :return: Another MergeableDict instance represents JSON schema of items
    """
    if typemap is None:
        typemap = _SIMPLETYPE_MAP

    if arr:
        return gen_schema(arr[0], typemap)
    else:
        return gen_schema("str", typemap)


def object_to_schema_nodes_iter(obj, typemap=None):
    """
    Generate a node represents JSON schema object with type annotation added
    for given object node.

    :param obj: Dict or MergeableDict object
    :param typemap: Type to JSON schema type mappings

    :yield: Another MergeableDict instance represents JSON schema of object
    """
    if typemap is None:
        typemap = _SIMPLETYPE_MAP

    for key, val in anyconfig.compat.iteritems(obj):
        yield (key, gen_schema(val, typemap=typemap))


def gen_schema(node, typemap=None):
    """
    Generate a node represents JSON schema object with type annotation added
    for given object node.

    :param node: Object node :: MergeableDict
    :param typemap: Type to JSON schema type mappings

    :return: Another MergeableDict instance represents JSON schema of this node
    """
    if typemap is None:
        typemap = _SIMPLETYPE_MAP

    ret = dict(type="null")

    if node is None:
        return ret

    _type = type(node)

    if _type in _SIMPLE_TYPES:
        ret = dict(type=typemap[_type])

    elif isinstance(node, dict):
        props = object_to_schema_nodes_iter(node, typemap)
        ret = dict(type=typemap[dict], properties=dict(props))

    elif _type in (list, tuple) or hasattr(node, "__iter__"):
        ret = dict(type=typemap[list],
                   items=array_to_schema_node(node, typemap))

    return ret

# vim:sw=4:ts=4:et:
