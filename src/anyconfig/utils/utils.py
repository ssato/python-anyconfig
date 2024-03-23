#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"""Misc utility functions."""
from __future__ import annotations

import typing


def noop(
    val: typing.Any, *_args, **_kwargs  # noqa: ANN002
) -> typing.Any:
    """Do nothing.

    >>> noop(1)
    1
    """
    return val


def filter_options(keys: typing.Iterable[str],
                   options: typing.Mapping[str, typing.Any]
                   ) -> typing.Dict[str, typing.Any]:
    """Filter 'options' with given 'keys'.

    :param keys: key names of optional keyword arguments
    :param options: optional keyword arguments to filter with 'keys'

    >>> filter_options(("aaa", ), {"aaa": 1, "bbb": 2})
    {'aaa': 1}
    >>> filter_options(("aaa", ), {"bbb": 2})
    {}
    """
    return {k: options[k] for k in keys if k in options}
