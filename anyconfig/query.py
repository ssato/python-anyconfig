#
# Copyright (C) 2017 Satoru SATOH <ssato redhat.com>
# License: MIT
#
r"""anyconfig.query module to support query data with JMESPath expressions.

Changelog:

.. versionadded:: 0.8.3

   - Added to query config data with JMESPath expression, http://jmespath.org
"""
from __future__ import absolute_import
try:
    import jmespath
except ImportError:
    pass

from anyconfig.globals import LOGGER


def query(data, **options):
    """
    Filter data with given JMESPath expression.

    See also: https://github.com/jmespath/jmespath.py and http://jmespath.org.

    :parae data: Target object (a dict or a dict-like object) to query
    :param options:
        Keyword option may include 'ac_query' which is a string represents
        JMESPath expression.

    :return: Maybe queried result data, primitive (int, str, ...) or dict
    """
    expression = options.get("ac_query", None)
    if expression is None or not expression:
        return data

    try:
        pexp = jmespath.compile(expression)
        return pexp.search(data)
    except ValueError as exc:  # jmespath.exceptions.*Error inherit from it.
        LOGGER.warn("Failed to compile or search: exp=%s, exc=%r",
                    expression, exc)
    except (NameError, AttributeError):
        LOGGER.warn("Filter module (jmespath) is not available. Do nothing.")

    return data

# vim:sw=4:ts=4:et:
