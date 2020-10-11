#
# Copyright (C) 2017, 2018 Satoru SATOH <ssato@redhat.com>
# Copyright (C) 2019 - 2020 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=bare-except
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


def query(data, jexp, **_options):
    """
    Filter data with given JMESPath expression.

    See also: https://github.com/jmespath/jmespath.py and http://jmespath.org.

    :param data: Target object (a dict or a dict-like object) to query
    :param jexp: a string represents JMESPath expression
    :param options: Keyword optios

    :return: A tuple of query result and maybe exception if failed
    """
    exc = None
    try:
        pexp = jmespath.compile(jexp)
        return (pexp.search(data), exc)

    except ValueError as exc:  # jmespath.exceptions.*Error inherit from it.
        return (data, exc)

    except (NameError, AttributeError) as exc:
        raise ValueError("Required 'jmespath' module is not available."
                         ) from exc

    except:  # noqa: E722
        return (None, exc)

# vim:sw=4:ts=4:et:
