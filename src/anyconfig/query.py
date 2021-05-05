#
# Copyright (C) 2017 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=bare-except
#
r"""anyconfig.query module to support query data with JMESPath expressions.

Changelog:

.. versionadded:: 0.8.3

   - Added to query config data with JMESPath expression, http://jmespath.org
"""
import typing

try:
    import jmespath
except ImportError:
    pass


DataT = typing.Mapping[str, typing.Any]


def query(data: DataT, jexp: str, **_options
          ) -> typing.Tuple[typing.Optional[DataT],
                            typing.Optional[Exception]]:
    """
    Filter data with given JMESPath expression.

    See also: https://github.com/jmespath/jmespath.py and http://jmespath.org.

    :param data: Target object (a dict or a dict-like object) to query
    :param jexp: a string represents JMESPath expression
    :param options: Keyword optios

    :return: A tuple of query result and maybe exception if failed
    """
    exc: typing.Optional[Exception] = None
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
