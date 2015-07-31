#
# Copyright (C) 2015 Satoru SATOH <ssato redhat.com>
# License: MIT
#
"""anyconfig.schema module.
"""
from __future__ import absolute_import
import logging
import anyconfig.compat

try:
    import jsonschema
except ImportError:
    pass


LOGGER = logging.getLogger(__name__)
_SIMPLETYPE_MAP = {list: "array", tuple: "array",
                   bool: "boolean",
                   int: "integer", float: "number",
                   dict: "object",
                   str: "string", unicode: "string"}


class ValidationError(Exception):
    """Generised validation error
    """
    pass


def _validate(obj, schema, format_checker=None):
    """
    Validate target object with given schema object, loaded from JSON schema.

    See also: https://python-jsonschema.readthedocs.org/en/latest/validate/

    :parae obj: Target object (a dict or a dict-like object) to validate
    :param schema: Schema object (a dict or a dict-like object)
        instantiated from schema JSON file or schema JSON string
    :param format_checker: A format property checker object of which class is
        inherited from jsonschema.FormatChecker, it's default if None given.

    :return: (True if validation succeeded else False, error message)
    """
    try:
        if format_checker is None:
            format_checker = jsonschema.FormatChecker()  # :raises: NameError
        try:
            jsonschema.validate(obj, schema, format_checker=format_checker)
        except (jsonschema.ValidationError, jsonschema.SchemaError) as exc:
            return (False, str(exc))

    except NameError:
        return (True, "Validation module (jsonschema) is not available")

    return (True, '')


def validate(obj, schema, format_checker=None):
    """
    Validate target object with given schema object, loaded from JSON schema.

    See also: https://python-jsonschema.readthedocs.org/en/latest/validate/

    :param obj: Object (a dict or a dict-like object) to validate
    :param schema: Schema object (a dict or a dict-like object)
        instantiated from schema JSON file or schema JSON string
    :param format_checker: A format property checker object of which class is
        inherited from jsonschema.FormatChecker, it's default if None given.

    :return: True if validation succeeded else False
    """
    (rc, msg) = _validate(obj, schema, format_checker)
    if msg:
        LOGGER.warn(msg)
    else:
        LOGGER.info("Validation succeeds")
    if not rc:
        raise ValidationError(msg)

    return True


def _array_to_schema_node(arr, typemap=None):
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


def _object_to_schema_nodes_iter(obj, typemap=None):
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

    if node is None:
        return dict(type="null")

    _type = type(node)

    if _type in (bool, int, float, str, unicode):
        return dict(type=typemap[_type])

    elif isinstance(node, dict):
        props = _object_to_schema_nodes_iter(node, typemap)
        return dict(type=typemap[dict], properties=dict(props))

    elif _type in (list, tuple) or hasattr(node, "__iter__"):
        return dict(type=typemap[list],
                    items=_array_to_schema_node(node, typemap))

    return dict(type="null")  # Default.

# vim:sw=4:ts=4:et:
